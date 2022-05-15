from rest_framework import serializers

from images.models import Image
from posts.models import Post, Comment, BookMark, TeamPost, TeamComment

# 이미 체크한 북마킹한 부분 피드백 필요!
class BookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = (
            'post',
            'user',
        )
        read_only_fields = (
            'post',
            'user',
        )
    def create(self, validated_data):
        validated_data["user"] = self.context.get("request").user
        validated_data["post_id"] = self.context.get("pk")
        return super().create(validated_data)


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            'image',
        )


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = (
            'id',
            'author',
            'title',
            'description',
            'images',
            'updated_at',
            'created_at',
        )
        read_only_fields=(
            'author',
        )

    def create(self, validated_data):
        validated_data["author"] = self.context.get("request").user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["author"] = self.context.get("request").user
        return super().update(instance, validated_data)

class PostScrapSummarizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = BookMark
        fields = (
            'id',
            'title',
            'nickname',
            'created_at',
            'updated_at',
            'images',
        )

class PostSummarizeSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = (
            'id',
            'images',
            'title',
            'created_at',
            'updated_at',
            'author',
            'comment_count',
        )

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            'author',
            'description',
            'post',
            'updated_at',
            'created_at',
        )
        read_only_fields = (
            'author',
        )

    def create(self, validated_data):
        validated_data["author"] = self.context.get("request").user
        return super().create(validated_data)

class TeamPostSerializer(serializers.ModelSerializer):
    images= ImageSerializer(read_only=True, many=True)
    class Meta:
        model = TeamPost
        fields = (
            'id',
            'team',
            'title',
            'description',
            'images',
            'updated_at',
            'created_at',
        )

class TeamPostSummarizeSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    class Meta:
        model = TeamPost
        fields = (
            'id',
            'images',
            'title',
            'created_at',
            'updated_at',
            'comment_count',
        )

class TeamCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamComment
        fields = (
            'author',
            'description',
            'post',
            'updated_at',
            'created_at',
        )
        read_only_fields = (
            'author',
        )

    def create(self, validated_data):
        validated_data["author"] = self.context.get("request").user
        return super().create(validated_data)