from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name = 'home'),
    path('tutorial/<slug:slug_title>', views.tutorial, name = 'tutorial'),
    path('article', views.article, name = 'article'),
    path('author/', views.author, name = 'author'),
    path('blog/<slug:slug_title>', views.edit_blog, name = 'edit_blog'),
    path('tutorial/claps/', views.claps, name = 'clap'),
    path('tutorial/', views.search, name = 'search')
]