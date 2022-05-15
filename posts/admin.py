from django.contrib import admin

from posts.models import Comment, Post, BookMark

admin.site.register([Post, Comment, BookMark])