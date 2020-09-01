from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Q
from ckeditor.fields import RichTextField


class BookManager(models.Manager):
    def search(self, query=None):
        qs = self.get_queryset()
        if query is not None:
            or_lookup = (Q(title__icontains=query) |
                         Q(content__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
        return qs


class Post(models.Model):
    title = models.CharField(verbose_name='标题', max_length=100)
    # content = models.TextField()
    content = RichTextField(verbose_name='内容')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})

    def get_content(self):
        if len(self.content) > 1000:
            return self.content[:1000] + '...'
        return self.content


class Book(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=100)
    publisher = models.CharField(max_length=100)
    url = models.URLField()

    objects = BookManager()

    def __str__(self):
        return self.title
