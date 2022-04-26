from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TeamViewSet, MemberViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r'team', TeamViewSet, basename='team')
member_router = DefaultRouter(trailing_slash=False)
member_router.register(r'member', MemberViewSet, basename='member')

urlpatterns = [
    path("", include(router.urls)),
    path("", include(member_router.urls)),
]