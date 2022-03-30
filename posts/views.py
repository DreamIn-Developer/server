from django.shortcuts import render
from rest_framework import viewsets

from posts.models import Post, Comment
from posts.seirlaizers import PostSerializer, PostSummarizeSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PostSummarizeSerializer
        else:
            return PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer