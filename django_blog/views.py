from django.shortcuts import render


def home(request):

    return render(request, 'django_blog/base.html')

def tutorial(request):

    return render(request, 'django_blog/blog.html')

def article(request):

    return render(request, 'django_blog/article.html')