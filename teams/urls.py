from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TeamViewSet, MemberAPIView

router = DefaultRouter(trailing_slash=False)
router.register(r'team', TeamViewSet, basename='team')

urlpatterns = [
    path("", include(router.urls)),
    path("member/<int:pk>", MemberAPIView.as_view()),
]