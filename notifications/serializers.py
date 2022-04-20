from rest_framework import serializers

from notifications.models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = (
            'id',
            'user',
            'messages',
            'is_read',
        )
        read_only_fiedls = (
            'id',
            'user',
            'messages',
        )

    def update(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        return super().update(validated_data)