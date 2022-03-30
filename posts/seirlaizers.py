from rest_framework import serializers

from posts.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'author',
            'description',
            'image',
            'updated_at',
            'created_at',
            'post_type',
        )

    def create(self, validated_data):
        validated_data["author"] = self.context.get("request").user
        return super().create(validated_data)

class PostSummarizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'image',
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

        def create(self, validated_data):
            validated_data["author"] = self.context.get("request").user
            return super().create(validated_data)