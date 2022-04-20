from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet, TeamPostViewSet, TeamCommentViewSet

posts_router = DefaultRouter(trailing_slash=False)
posts_router.register(r'posts', PostViewSet, basename='post')
comments_router = DefaultRouter(trailing_slash=False)
comments_router.register(r'comments', CommentViewSet, basename='comment')
bookmark_router = DefaultRouter(trailing_slash=False)
team_posts_router = DefaultRouter(trailing_slash=False)
team_posts_router.register(r'teams/posts', TeamPostViewSet, basename='team_posts')
team_comments_router = DefaultRouter(trailing_slash=False)
team_comments_router.register(r'teams/comments', TeamCommentViewSet, basename='team_comments')
urlpatterns = [
    path("", include(posts_router.urls)),
    path("", include(comments_router.urls)),
    path("", include(team_posts_router.urls)),
    path("", include(team_comments_router.urls)),
]