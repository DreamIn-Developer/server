from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action

from images.models import Image
from posts.models import Post, Comment, TeamPost, TeamComment, BookMark, PostLike, TeamPostLike
from posts.seirlaizers import PostSerializer, PostSummarizeSerializer, CommentSerializer, \
    TeamPostSummarizeSerializer, TeamCommentSerializer, TeamPostSerializer, PostRetrieveSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PostSummarizeSerializer
        elif self.action == 'comments':
            return CommentSerializer
        elif self.action == 'retrieve':
            return PostRetrieveSerializer
        else:
            return PostSerializer

    def create(self, request, *args, **kwargs):
        images = request.data.get('images', None)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        if images:
            for image in images:
                _image, _ = Image.objects.get_or_create(image=image)
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
            instance.images.clear()
            for image in images:
                _image, _ = Image.objects.get_or_create(image=image)
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

    @action(detail=True, methods=['post'])
    def scrap(self, request, pk):
        scrap = BookMark.objects.filter(user=request.user, post_id=pk).first()
        if scrap:
            scrap.delete()
            return Response({'message': "cancel scrap"}, status=status.HTTP_204_NO_CONTENT)
        else:
            BookMark.objects.create(user=request.user, post_id=pk)
            return Response({'message': 'success scrap'}, status=status.HTTP_201_CREATED)
        return Response({'error_message': 'request data error'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def main(self, request):
        queryset = Post.objects.all().order_by('?')
        serializer = PostSummarizeSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def like(self, request, pk):
        like = PostLike.objects.filter(user=request.user, post_id=pk).first()
        if like:
            like.delete()
            return Response({'message': "cancel like"}, status=status.HTTP_204_NO_CONTENT)
        else:
            PostLike.objects.create(user=request.user, post_id=pk)
            return Response({'message': 'success like'}, status=status.HTTP_201_CREATED)
        return Response({'error_message': 'request data error'}, status=status.HTTP_400_BAD_REQUEST)


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
                _image, _ = Image.objects.get_or_create(image=image)
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
            instance.images.clear()
            for image in images:
                _image, _ = Image.objects.get_or_create(image=image)
                instance.images.add(_image)
        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk):
        comments = TeamComment.objects.filter(post__id=pk)
        serializer = TeamCommentSerializer(comments, many=True, context={'request': request, 'pk': pk})
        return Response(serializer.data, status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def like(self, request, pk):
        like = TeamPostLike.objects.filter(user=request.user, team_post_id=pk).first()
        if like:
            like.delete()
            return Response({'message': "cancel like"}, status=status.HTTP_204_NO_CONTENT)
        else:
            TeamPostLike.objects.create(user=request.user, team_post_id=pk)
            return Response({'message': 'success like'}, status=status.HTTP_201_CREATED)
        return Response({'error_message': 'request data error'}, status=status.HTTP_400_BAD_REQUEST)


class TeamCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TeamCommentSerializer
    queryset = TeamComment.objects.all()
