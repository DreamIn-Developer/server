from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from images.models import Image
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

    def create(self, request, *args, **kwargs):
        images = request.data.get('images', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        if images:
            for image in images:
                _image = Image.objects.create(image=image)
                instance.images.add(_image)
        else:
            instance
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance

    def update(self, request, *args, **kwargs):
        images = request.data.get('images', None)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        if images:
            for image in images:
                _image = Image.objects.get_or_create(image)
                instance.images.clear()
                instance.images.add(_image)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

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

    def create(self, request, *args, **kwargs):
        images = request.data.get('images', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        if images:
            for image in images:
                _image = Image.objects.create(image=image)
                instance.images.add(_image)
        else:
            instance
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance

    @action(detail=True, methods=['get'])
    def comments(self, request, pk):
        comments = TeamComment.objects.filter(post__id=pk)
        serializer = TeamCommentSerializer(comments, many=True, context={'request': request, 'pk': pk})
        return Response(serializer.data, status.HTTP_200_OK)


class TeamCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TeamCommentSerializer
    queryset = TeamComment.objects.all()
