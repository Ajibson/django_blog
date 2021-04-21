from django import forms
from django.core.exceptions import ValidationError
from django.db.models import fields
from .models import *
from django.utils.translation import ugettext_lazy as _




class ArticleForm(forms.ModelForm):

    class Meta:
        model = blogs
        fields = "__all__"

class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = "__all__"

    password = forms.PasswordInput()


    def clean_email(self):
        email = self.cleaned_data.get("email")
        db_email = User.objects.filter(email__iexact=email)
        if db_email:
            raise ValidationError("Email already exist")
        return email

    

    

