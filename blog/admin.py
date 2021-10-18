from django.contrib import admin
from .models import Post, Book

admin.site.register(Post)



@admin.register(Book)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'publisher')
    search_fields = ('title',  'author')

