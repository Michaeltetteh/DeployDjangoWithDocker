import django
from django.shortcuts import render,redirect
from .models import Movie,Person,Vote
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


from .forms import (
    VoteForm,
    MovieImageForm,
)

from .mixins import CachePageVaryOnCookieMixin
from django.core.cache import cache




class MovieListView(CachePageVaryOnCookieMixin,ListView):
    model = Movie
    paginate_by = 10

    def get_context_data(self, **kwargs):
        ctx = super(MovieListView,self).get_context_data(**kwargs)
        page = ctx['page_obj']
        paginator = ctx['paginator']
        ctx['page_is_first'] = (page.number == 1)
        ctx['page_is_last'] = (page.number == paginator.num_pages)
        return ctx

class MovieDetail(DetailView):
    queryset = Movie.object.all_with_related_persons_and_score()

    def get_context_data(self,**kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['image_form'] = self.movie_image_form()
        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie = self.object,
                user = self.request.user)
            if vote.id:
                vote_form_url = reverse('core:UpdateVote',kwargs={'movie_id':vote.movie.id,'pk': vote.id})
            else:
                vote_form_url = (reverse('core:CreateVote',kwargs={'movie_id': self.object.id}))

            vote_form = VoteForm(instance=vote)
            ctx['vote_form'] = vote_form
            ctx['vote_form_url'] = vote_form_url
            return ctx
    #helper
    def movie_image_form(self):
        if self.request.user.is_authenticated:
            return MovieImageForm()
        return None
class PersonDetail(DetailView):
    queryset = Person.object.all_with_prefetch_movies()


class CreateVote(LoginRequiredMixin,CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail',kwargs={'pk':movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail',kwargs={'pk':movie_id})
        return redirect(to=movie_detail_url)


class UpdateVote(LoginRequiredMixin,UpdateView):
    form_class = VoteForm

    queryset = Vote.objects.all()
    
    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied('cannot change another user\'s vote')
        return vote
    
    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:MovieDetail',kwargs={'pk':movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = context['object'].id
        movie_detail_url = reverse('core:MovieDetail',kwargs={'pk':movie_id})
        return redirect(to=movie_detail_url)


class MovieImageUpload(LoginRequiredMixin,CreateView):
    form_class = MovieImageForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs['movie_id']
        return initial
    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail',kwargs={'pk':movie_id})
        return redirect(to=movie_detail_url)

    def get_success_url(self):
        movie_id = self.kwargs['movie_id']
        movie_detail_url = reverse('core:MovieDetail',kwargs={'pk':movie_id})

        return movie_detail_url



class TopMovies(CachePageVaryOnCookieMixin,ListView):
    template_name = 'core/top_movie_list.html'

    def get_queryset(self):
        limit = 10
        key = 'top_movies_%s' % limit 
        cached_qs = cache.get(key)
        if cached_qs:
            same_django = cached_qs._django_version == django.get_version()
            if same_django:
                return cached_qs
        qs = Movie.object.top_movies(limit=limit)
        cache.set(key,qs)
        return qs


