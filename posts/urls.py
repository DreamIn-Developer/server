from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet

posts_router = DefaultRouter(trailing_slash=False)
posts_router.register(r'posts', PostViewSet, basename='post')
comments_router = DefaultRouter(trailing_slash=False)
comments_router.register(r'comments', CommentViewSet, basename='comment')
bookmark_router = DefaultRouter(trailing_slash=False)
urlpatterns = [
    path("", include(posts_router.urls)),
    path("", include(comments_router.urls)),
]