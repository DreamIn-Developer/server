from django.contrib import admin

from posts.models import Comment, Post, BookMark, PostLike, TeamPostLike, TeamPost, TeamBookMark

admin.site.register([Post, Comment, BookMark, PostLike, TeamPostLike, TeamPost, TeamBookMark])