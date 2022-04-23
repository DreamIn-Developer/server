from rest_framework import serializers
from .models import User, FollowRelation, Category

# 이미 팔로우하고 있을때를 구별해야함
#
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowRelation
        fields = (
            'follower',
            'following',
        )
        read_only_fields = (
            'follower',
            'following',
        )

    def create(self,instance, validated_data):
        validated_data["follower"] = self.context.get("request").user
        validated_data["following_id"] = self.context.get("pk")
        return super().create(validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'main_category',
            'sub_category',
        )

class UserSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'nickname',
            'description',
            'image',
            'categories',
            'post_count',
            'scrap_count',
            'follower_count',
            'following_count',
        )
        read_only_fields = (
            'post_count',
            'scrap_count',
            'follower_count',
            'following_count',
        )

class SocialLoginSerializer(serializers.ModelSerializer):
    access_token = serializers.CharField(max_length=63)
    class Meta:
        model = User
        fields = (
            'id',
            'access_token',
            'nickname',
            'social_type',
            'social_id',
        )
        read_only_fields = (
            'id',
            'nickname',
            'social_type',
            'social_id',
        )