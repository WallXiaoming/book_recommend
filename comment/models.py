from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from blog.models import Post

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_on = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=False)
    body = models.TextField(verbose_name='内容')

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.author.username)