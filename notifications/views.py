from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,GenericViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer

    @swagger_auto_schema(operation_summary="알림 리스트", operation_description='알림 리스트 확인하는 api')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="알림 상세보기", operation_description='알림 내용 상세보기 api')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="알림 읽은 필드 표시", operation_description='patch 또는 put으로 iS_read 필드 True 변경!')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)