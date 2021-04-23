from django.test import TestCase,Client, client
from django.urls import reverse
from django_blog.models import User, comment, clap, blogs
import json


class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')

        Blogs = blogs.objects.filter(status = 'Published').order_by('-date_published')
    
    def test_blogs_list(self):
        response = self.client.get(self.home_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_blog/base.html')