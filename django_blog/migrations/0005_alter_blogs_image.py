# Generated by Django 3.2 on 2021-04-24 10:27

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('django_blog', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogs',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='PNG', keep_meta=True, quality=0, size=[3000, 1740], upload_to='article_pics'),
        ),
    ]
