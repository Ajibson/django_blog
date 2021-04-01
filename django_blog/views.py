from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages

def home(request):
    try:
        articles = blogs.objects.all()
    except blogs.DoesNotExist:
        messages.error(request, 'No blog post')
        return redirect('home')
    return render(request, 'django_blog/base.html', {'articles':articles})

def tutorial(request,slug_title):
    try:
        article = blogs.objects.get(slug = slug_title)
    except blogs.DoesNotExist:
        messages.error(request, 'No blog post')
        return redirect('home')
    return render(request, 'django_blog/blog.html', {'article':article})

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
