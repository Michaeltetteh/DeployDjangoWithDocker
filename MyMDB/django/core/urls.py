from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('movie',views.MovieListView.as_view(), name='MovieListView'),
    path('movie/<int:pk>',views.MovieDetail.as_view(),name='MovieDetail'),
    
]