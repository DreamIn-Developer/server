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

    @swagger_auto_schema(operation_summary="개인프로필 게시글 리스트 조회", operation_description='개인 프로필의 게시글을 조회하는 api')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="게시글 삭제")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="개인 프로필 단일 조회", operation_description='해당 id값의 개프로필 조회 api입니다.')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="개인 프로필 게시글 생성", operation_description='헤더 토큰 필수!')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="개인 프로필 게시글 수정",
                         operation_description='개인 프로필 게시글 수정 api입니다. 헤더 토큰 필수! 팀에 속한 유저만 수정가능합니다.')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    @swagger_auto_schema(operation_summary="해당 게시글의 댓글 조회", operation_description='게시글 id값에 해당하는 댓글 조회 아피')
    @action(detail=True, methods=['get'])
    def comments(self, request, pk):
        comments = Comment.objects.filter(post__id=pk)
        serializer = CommentSerializer(comments, many=True, context={'request': request, 'pk': pk})
        return Response(serializer.data, status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="스크랩 하기", operation_description='해당 게시글을 스크랩하는 api입니다. 헤더토큰 필수!')
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

    @swagger_auto_schema(operation_summary="댓글 리스트 조회(전체)", operation_description='게시글에 상관없이 모든 댓글 조회 api')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="댓글 삭제")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="댓글 상세보기", operation_description='해당 id값의 댓글 조회 api입니다.')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="댓글 생성", operation_description='헤더 토큰 필수!')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="댓글 수정",
                         operation_description='댓글 수정 api입니다. 헤더 토큰 필수! 생성한 유저만 수정 가능합니다.')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

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