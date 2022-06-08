from django.contrib import admin

from posts.models import Comment, Post, BookMark, PostLike, TeamPostLike

admin.site.register([Post, Comment, BookMark, PostLike, TeamPostLike])