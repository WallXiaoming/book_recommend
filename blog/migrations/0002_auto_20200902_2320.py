# Generated by Django 3.0.8 on 2020-09-02 15:20

from django.db import migrations
import martor.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=martor.models.MartorField(verbose_name='内容'),
        ),
    ]
