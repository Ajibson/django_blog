from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name = 'home'),
    path('tutorial/<slug:slug_title>', views.tutorial, name = 'tutorial'),
    path('article', views.article, name = 'article'),
    path('author/', views.author, name = 'author'),
    path('blog/<slug:slug_title>', views.edit_blog, name = 'edit_blog'),
    path('tutorial/claps/', views.claps, name = 'clap'),
    path('tutorial/', views.search, name = 'search'),
    path('django_way/signup', views.signup, name = 'signup'),
    path('django_way/login', views.Login, name = 'login'),
    path('home', views.logout_user, name = 'logout_user'),
    path('comment_form', views.comments, name = 'comment_form'),
    path('reset_password/', views.reset_password, name = 'reset_password'),
    path("password_reset/", views.password_reset_request, name="Reset_password"),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),   
]