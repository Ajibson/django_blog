from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages

def home(request):

    return render(request, 'django_blog/base.html')

def tutorial(request):

    return render(request, 'django_blog/blog.html')

def article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article saved successfully')
            return redirect('article')
    else:
        form = ArticleForm()
        articles = blogs.objects.all()
    return render(request, 'django_blog/article.html', {'form':form, 'articles':articles})

def author(request):

    return render(request, 'django_blog/author.html')

def edit_blog(request, slug_title):
    if request.method == 'POST':
        article = blogs.objects.get(slug = slug_title)
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, 'Article edited successfully')
            return redirect('article')
    else:
        form = ArticleForm()
        article = blogs.objects.get(slug = slug_title)
    return render(request, 'django_blog/edit_article.html', {'form':form, 'article':article})
