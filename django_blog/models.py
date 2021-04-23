from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django_blog.utils.blog_utils import count_words, read_time
from django_resized import ResizedImageField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save

class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True)
    email = models.EmailField(verbose_name = 'email', max_length=255, unique=True)
    password = models.CharField(max_length=100, unique=True, blank=True)
    date_joined = models.DateTimeField(default = timezone.now, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'password','username'
    ]

    def get_email(self):
        return self.email

class IpModel(models.Model):
    ip = models.CharField(max_length = 150)

    def __str__(self):
        return self.ip

class blogs(models.Model):
    status_choice = (
        ('Drafted', 'Drafted'),('Published', 'Published')
    )
    title = models.CharField(max_length=500)
    date_published = models.DateField(default = timezone.now, blank=True)
    date_created = models.DateField(default = timezone.now, blank=True)
    author = models.CharField(max_length=200, default='Aremu Azeez Taiwo', blank=True)
    image = ResizedImageField(size=[3000, 1740], upload_to='article_pics',force_format='PNG')
    content = RichTextUploadingField(blank=True)
    slug = models.SlugField(blank=True)
    tags = TaggableManager(blank=True)
    status = models.CharField(max_length=20, choices=status_choice,default='DRAFT')
    views = models.ManyToManyField(IpModel,  blank = True)
    count_words = models.CharField(max_length=50, default=0, blank=True)
    read_time = models.CharField(max_length=50, default=0, blank=True)
    deleted = models.BooleanField(default=False,blank=True)

    class Meta:
        ordering = ('-date_published',)
        verbose_name_plural = 'blogs'

    def __str__(self):
        return self.title 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        self.count_words = count_words(self.content)
        self.read_time = read_time(self.content)
        super(blogs, self).save(*args, **kwargs)


class clap(models.Model):
    blog = models.ForeignKey(blogs, on_delete=models.CASCADE)
    number_of_clap = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return (self.blog.title + "   " + str(self.number_of_clap) + ' claps')

#class comment(models.Model):

@receiver(post_save, sender=User)
def activate_user(sender, instance, created, **kwargs):
    print(instance)
    if created:
        instance.is_active = True
        instance.save()

class comment(models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    content = models.TextField()
    date_commented = models.DateTimeField(default=timezone.now, blank=True)
    article = models.ForeignKey(blogs, on_delete=models.CASCADE, blank=True)
    reply = models.TextField(blank = True)

    def __str__(self):
        return self.content


