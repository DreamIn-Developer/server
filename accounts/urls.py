from django.urls import path, include
from rest_framework.routers import DefaultRouter

from accounts.views import UserViewSet, CategoryAPIView

router = DefaultRouter(trailing_slash=False)
router.register(r'users', UserViewSet, basename='users')
category_router = DefaultRouter(trailing_slash=False)
category_router.register(r'category', CategoryAPIView, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(category_router.urls)),
]