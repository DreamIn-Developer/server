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