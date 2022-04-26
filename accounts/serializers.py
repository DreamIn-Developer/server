from rest_framework import serializers
from .models import User, FollowRelation, MainCategory, SubCategory

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

    def create(self, validated_data):
        validated_data["follower"] = self.context.get("request").user
        validated_data["following_id"] = self.context.get("pk")
        return super().create(validated_data)

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = (
            'id',
            'name',
        )

class CategorySerializer(serializers.ModelSerializer):
    sub_category = serializers.SerializerMethodField()
    class Meta:
        model = MainCategory
        fields = (
            'id',
            'main_category',
            'sub_category',
        )
        read_only_fields = (
            'main_category',
            'sub_category',
        )
    def get_sub_category(self, obj):
        serializer = SubCategorySerializer(obj.subcategory, many=True)
        return serializer.data

class UserSerializer(serializers.ModelSerializer):
    categories = SubCategorySerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'nickname',
            'description',
            'profile_image',
            'background_image',
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