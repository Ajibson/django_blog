from django.test import SimpleTestCase
from django.urls import reverse,resolve
from django_blog.views import home,signup,Login,tutorial,article,author,edit_blog,claps,logout_user,comments,reset_password


class TestUrl(SimpleTestCase):

    def test_url_home(self):
         url = reverse('home')
         self.assertEqual(resolve(url).func, home)

    def test_url_signup(self):
         url = reverse('signup')
         self.assertEqual(resolve(url).func, signup)

    def test_url_Login(self):
         url = reverse('login')
         self.assertEqual(resolve(url).func, Login)
        
    def test_url_totorial(self):
         url = reverse('tutorial', args=['slug-value'])
         self.assertEqual(resolve(url).func, tutorial)

    def test_url_article(self):
         url = reverse('article')
         self.assertEqual(resolve(url).func, article)

    def test_url_edit_blog(self):
         url = reverse('edit_blog' , args=['slug-value'])
         self.assertEqual(resolve(url).func, edit_blog) 
        
    def test_url_author(self):
         url = reverse('author')
         self.assertEqual(resolve(url).func, author) 

    def test_url_clap(self):
         url = reverse('clap')
         self.assertEqual(resolve(url).func, claps) 

    def test_url_logout_user(self):
         url = reverse('logout_user')
         self.assertEqual(resolve(url).func, logout_user) 

    def test_url_commentform(self):
         url = reverse('comment_form')
         self.assertEqual(resolve(url).func, comments) 

    def test_url_reset_password(self):
         url = reverse('reset_password')
         self.assertEqual(resolve(url).func, reset_password) 