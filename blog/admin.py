from django.db import models
from django.contrib import admin
from .models import Post, Book
from martor.widgets import AdminMartorWidget

class PostModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': AdminMartorWidget},
    }

admin.site.register(Post, PostModelAdmin)
admin.site.register(Book)
