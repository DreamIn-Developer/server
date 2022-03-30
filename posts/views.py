from django.shortcuts import render
from requests import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from posts.models import Post, Comment
from posts.seirlaizers import PostSerializer, PostSummarizeSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PostSummarizeSerializer
        else:
            return PostSerializer

    @action(detail=True, methods=['get'])
    def comments(self, request, pk):
        comments = Comment.objects.filter(post__id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer