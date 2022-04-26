from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from posts.models import Post, Comment, TeamPost, TeamComment
from posts.seirlaizers import PostSerializer, PostSummarizeSerializer, CommentSerializer, BookMarkSerializer, \
    TeamPostSummarizeSerializer, TeamCommentSerializer, TeamPostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PostSummarizeSerializer
        elif self.action == 'comments':
            return CommentSerializer
        else:
            return PostSerializer

    @action(detail=True, methods=['get'])
    def comments(self, request, pk):
        comments = Comment.objects.filter(post__id=pk)
        serializer = CommentSerializer(comments, many=True, context={'request': request, 'pk': pk})
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def me(self, request):
        posts = Post.objects.filter(author=request.user)
        serializer = PostSummarizeSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def scrap(self, request, pk):
        serializer = BookMarkSerializer(data=request.data, context={'request': request, 'pk': pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class TeamPostViewSet(viewsets.ModelViewSet):
    queryset = TeamPost.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamPostSummarizeSerializer
        elif self.action == 'comments':
            return TeamCommentSerializer
        else:
            return TeamPostSerializer

    @action(detail=True, methods=['get'])
    def comments(self, request, pk):
        comments = TeamComment.objects.filter(post__id=pk)
        serializer = TeamCommentSerializer(comments, many=True, context={'request': request, 'pk': pk})
        return Response(serializer.data, status.HTTP_200_OK)

class TeamCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TeamCommentSerializer
    queryset = TeamComment.objects.all()