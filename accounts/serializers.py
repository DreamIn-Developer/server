from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'nickname',
            'description',
            'image',
        )

class SocialLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'social_type',
            'social_id'
        )