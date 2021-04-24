from django.test import TestCase,Client, client
from django.urls import reverse
from django_blog.models import User, comment, clap, blogs
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.tutorial = reverse('tutorial', args=['django-crud-actions'])
        self.article = reverse('article')
        Blogs = blogs.objects.filter(status = 'Published').order_by('-date_published')

        self.blog1 = blogs.objects.create(
            title = 'Django Crud Actions',
            status = 'Published',
            slug = 'django-crud-actions',
            image = 'C:/Users/TEMP/Pictures/Screenshots/one.png'
        )

        self.clap1 = clap.objects.create(
            blog = self.blog1,
            number_of_clap = 3
        )
    
    #check home view running as expected 
    # This will fail snce we have to supplied login parameters
    def test_blogs_list(self):
        response = self.client.get(self.home_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_blog/base.html') #Check if the template being used is base.html

    def test_tutorial_view(self):
        
        response = self.client.get(self.tutorial)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_blog/blog.html')

    def test_blog_view(self):
        
        response = self.client.post(self.article, {
            'title' : 'Djangos Crud Actions',
            'status' : 'Published',
            'slug' : 'djangos-crud-actions',
            'image' : 'C:/Users/TEMP/Pictures/Screenshots/one.png'
        })

        self.assertEqual(response.status_code, 200)
        #self.assertTemplateUsed(response, 'django_blog/blog.html')
    