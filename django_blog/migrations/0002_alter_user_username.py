# Generated by Django 3.2 on 2021-04-21 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, max_length=150, unique=True),
        ),
    ]
