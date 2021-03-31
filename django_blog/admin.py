from django.contrib import admin
from .models import *


@admin.register(IpModel)
class IpmodelAdmin(admin.ModelAdmin):
    pass

@admin.register(blogs)
class blogsAdmin(admin.ModelAdmin):
    pass
