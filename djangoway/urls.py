from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views


handler404 = 'django_blog.views.view_404' 
handler500 = 'django_blog.views.view_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
        path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)