from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 

handler404 = 'django_blog.views.view_404' 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('django_blog.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)