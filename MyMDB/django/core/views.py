from django.shortcuts import render
from core.models import Movie
from django.views.generic import (
    ListView,
    DetailView,
)

class MovieListView(ListView):
    model = Movie
    # template_name = "movie_list"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        ctx = super(MovieListView,self).get_context_data(**kwargs)
        page = ctx['page_obj']
        paginator = ctx['paginator']
        ctx['page_is_first'] = (page.number == 1)
        ctx['page_is_last'] = (page.number == paginator.num_pages)
        return ctx

class MovieDetail(DetailView):
    model = Movie

