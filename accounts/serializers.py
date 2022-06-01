from rest_framework import serializers
from .models import User, MainCategory, SubCategory, FollowRelation


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
    categories = SubCategorySerializer(many=True, read_only=True)
    is_followed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'nickname',
            'description',
            'profile_image',
            'background_image',
            'categories',
            'post_count',
            'scrap_count',
            'follower_count',
            'following_count',
            'is_followed',
        )
        read_only_fields = (
            'post_count',
            'scrap_count',
            'follower_count',
            'following_count',
            'is_followed',
        )

    def get_is_followed(self, obj):
        login_user = self.context.get("request").user.id
        if login_user != None:
            is_followed = FollowRelation.objects.filter(follower=login_user, following_id=obj).first()
            if is_followed is None:
                return False
            else:
                return True
        else:
            return False


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
