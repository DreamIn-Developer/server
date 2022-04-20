from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from notifications.models import Notification
from notifications.serializers import NotificationSerializer


class NotificationViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,GenericViewSet):
    lookup_field = 'notification_pk'
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer