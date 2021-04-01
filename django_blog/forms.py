from django import forms
from .models import *



class ArticleForm(forms.ModelForm):

    class Meta:
        model = blogs
        fields = "__all__"