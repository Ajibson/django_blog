from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.http import HttpResponse, request
import json
from django.db.models import Q
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data.get("email")
            user.username = username
            user.set_password(form.cleaned_data.get("password"))
            user.save()
            return redirect("home")
        else:
            return render(request, 'django_blog/signup.html', {'form':form})
    else:
        form = SignupForm()
    return render(request, 'django_blog/signup.html', {'form':form})

def Login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(email = form.cleaned_data.get("email"), password = form.cleaned_data.get("password"))
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                msg = "Invaid credential supplied"
                return render(request, 'django_blog/login.html', {'form':form, 'msg':msg})
        else:
            return render(request, 'django_blog/login.html', {'form':form})
    else:
        form = LoginForm()
    return render(request, 'django_blog/login.html', {'form':form})




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

def logout_user(request):
    logout(request)
    return redirect('login')

def tutorial(request,slug_title):
    try:
        articles = blogs.objects.filter(status = 'Published').order_by('-date_published')
        article = blogs.objects.get(slug = slug_title)
        number_of_claps = clap.objects.get(blog = article.pk).number_of_clap
        comments = comment.objects.filter(article = article).order_by('-date_commented')
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
    return render(request, 'django_blog/blog.html', {'article':article, 'claps':number_of_claps, 'articles':articles, 'comments':comments})

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
    for word in q: #if user input 'python django' q = ['python', 'django']
        query = query | Q(title__icontains=word, status = 'Published') | Q(tags__name__icontains=word, status = 'Published')
    print(query)
    results = blogs.objects.filter(query).distinct()
    return render(request, 'django_blog/base.html', {'articles':results})

def view_404(request, exception):

    return render(request, '404.html')

@login_required
def comments(request):

    if request.method == "POST":
        article = blogs.objects.get(pk = request.POST.get('blog_id')) #Article primary key
        name = request.user
        content = request.POST.get("content")
        new_comment = comment(name = name, content = content, article = article)
        new_comment.save()
        

    return HttpResponse("Hello")

@login_required
def reset_password(request):
    if request.method == "POST":
        form = password_resetForm(request.POST)
        if form.is_valid():
            user = request.user
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            logout(request)
            return redirect("login")
        else:
            return render(request, 'django_blog/reset_password.html', {'form':form})
    else:
        form = password_resetForm()

    return render(request, 'django_blog/reset_password.html', {'form':form})


def view_500(request):
    return render(request, '500.html')


def password_reset_request(request):
    if request.method == "POST":
        form = ResetForms(request.POST)
        if form.is_valid():
            data = form.cleaned_data.get('email')
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "registration/password_reset_email.html"
                    c = {
                    "email":user.email,
                    'domain':'zuri-task.herokuapp.com',
                    'site_name': 'zuri-task.herokuapp.com',
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    'token': default_token_generator.make_token(user),
                    'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'myvtuservice@gmail.com' , [user.email], fail_silently=False)
                        return redirect("password_reset_done")
                    except BadHeaderError:
                        messages.error(request, 'please try again')
                        return redirect('reset_password')
            else:
                messages.error(request, 'The email is not registered')
                return redirect('Reset_password')                         
    else:
        form = ResetForms()
    return render(request, "registration/password_reset_form.html", {"password_reset_form":form})

def password_reset_confirm(request,uidb64,token):
    user_pk = json.loads(urlsafe_base64_decode(uidb64))
    user = User.objects.get(pk=user_pk)
    if request.method == 'POST':
        form = NewPasswordResetForm(request.POST)
        if form.is_valid():
            password1 = form.cleaned_data['password1']
            user.set_password(password1)
            user.save()
            return redirect('password_reset_complete')
    else:
        form = NewPasswordResetForm()
    return render(request, 'registration/password_reset_confirm.html', {'form':form})  
