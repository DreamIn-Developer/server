from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TeamViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'team', TeamViewSet, basename='team')

urlpatterns = [
    path("", include(router.urls)),
]