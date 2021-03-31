from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from django.utils.text import slugify
from django_blog.utils.blog_utils import count_words, read_time
from django_resized import ResizedImageField
from django.utils import timezone

class IpModel(models.Model):
    ip = models.CharField(max_length = 150)

    def __str__(self):
        return self.ip

class blogs(models.Model):
    status_choice = (
        ('Drafted', 'Drafted'),('Published', 'Published')
    )
    title = models.CharField(max_length=500)
    date_published = models.DateField(default = timezone.now)
    date_created = models.DateField(default = timezone.now)
    author = models.CharField(max_length=200, default='Aremu Azeez Taiwo')
    image = ResizedImageField(size=[3000, 1740], upload_to='article_pics',force_format='PNG')
    content = RichTextUploadingField(blank=True)
    slug = models.SlugField()
    tags = TaggableManager(blank=True)
    status = models.CharField(max_length=20, choices=status_choice,
                              default='DRAFT')
    views = models.ManyToManyField(IpModel,  blank = True)
    count_words = models.CharField(max_length=50, default=0)
    read_time = models.CharField(max_length=50, default=0)
    deleted = models.BooleanField(default=False)

    class Meta:
        ordering = ('-date_published',)
        verbose_name_plural = 'blogs'

    def __str__(self):
        return self.title 

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        self.count_words = count_words(self.content)
        self.read_time = read_time(self.content)

