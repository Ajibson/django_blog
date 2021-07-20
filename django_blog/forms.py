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

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise ValidationError("Length of password is less than 8")
        if password.isalpha():
            raise ValidationError("Password should contains both letters and numbers")
        if password.isnumeric():
            raise ValidationError("Password should contains both letters and numbers")
        return password


class LoginForm(forms.Form):
    email = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(),max_length=20)

class password_resetForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(),max_length=20)
    password2 = forms.CharField(widget=forms.PasswordInput(),max_length=20)

    def clean(self):
        cleaned_data = super(password_resetForm, self).clean()
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        print(password, password2)
        if len(password) < 8:
            raise forms.ValidationError({"password":"Length of password is less than 8"})
        if password.isalpha():
            raise ValidationError({"password":"Password should contains both letters and numbers"})
        if password.isnumeric():
            raise ValidationError({"password":"Password should contains both letters and numbers"})
        if password != password2:
            raise ValidationError({"password":"Password must match"})
        
        return cleaned_data


        


class ResetForms(forms.Form):
    email = forms.EmailField()


        
class NewPasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    
    def clean(self):
        cleaned_data = super(password_resetForm, self).clean()
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        print(password, password2)
        if len(password) < 8:
            raise ValidationError("Length of password is less than 8")
        if password.isalpha():
            raise ValidationError("Password should contains both letters and numbers")
        if password.isnumeric():
            raise ValidationError("Password should contains both letters and numbers")
        if password != password2:
            raise ValidationError(_("Password must match"))
        
        return cleaned_data






    

    

