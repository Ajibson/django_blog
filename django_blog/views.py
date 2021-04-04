from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
import json
from django.db.models import Q


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    try:
        articles = blogs.objects.filter(status = 'Published').order_by('-date_published')
    except blogs.DoesNotExist:
        messages.error(request, 'No blog post')
        return render(request, 'django_blog/base.html')
    return render(request, 'django_blog/base.html', {'articles':articles})

def tutorial(request,slug_title):
    try:
        articles = blogs.objects.filter(status = 'Published').order_by('-date_published')
        article = blogs.objects.get(slug = slug_title)
        number_of_claps = clap.objects.get(blog = article.pk).number_of_clap
        ip = get_client_ip(request)
        ip_check = [i.ip for i in article.views.all()]
        if IpModel.objects.filter(ip = ip).exists() and ip in ip_check:
            pass
        elif ip in ip_check:
            pass
        elif not IpModel.objects.filter(ip = ip).exists():
            IpModel.objects.create(ip = ip)
            article.views.add(IpModel.objects.get(ip = ip))
        else:
            article.views.add(IpModel.objects.get(ip = ip))
    except (blogs.DoesNotExist, clap.DoesNotExist):
        messages.error(request, 'No blog post')
        return render(request, 'django_blog/base.html')
    return render(request, 'django_blog/blog.html', {'article':article, 'claps':number_of_claps, 'articles':articles})

def article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            post = clap(number_of_clap=0, blog=blogs.objects.get(title = request.POST.get('title')))
            post.save()
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




def claps(request):
    if request.method == 'POST':
        post_clap = request.POST.get('number_of_clap')
        blog_slug = request.POST.get('blog')
        response_data = {}
        post = clap.objects.get(blog=blogs.objects.get(slug = blog_slug))
        post.number_of_clap =  int(post_clap) + 1
        post.save()
        response_data['result'] = 'Create post successful!'
        response_data['postpk'] = post.pk
        response_data['text'] = post.number_of_clap

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def search(request):
    q = request.GET['search_value'].split()  # I am assuming space separator in URL like "random stuff"
    query = Q()
    for word in q:
        query = query | Q(title__icontains=word, status = 'Published') | Q(tags__name__icontains=word, status = 'Published')
    results = blogs.objects.filter(query).distinct()

    return render(request, 'django_blog/base.html', {'articles':results})


