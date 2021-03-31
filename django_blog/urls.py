from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('tutorial', views.tutorial, name = 'tutorial'),
    path('article', views.article, name = 'article')
]