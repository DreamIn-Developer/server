from rest_framework import serializers

from posts.models import Post, Comment, BookMark, TeamPost, TeamComment


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

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'author',
            'title',
            'description',
            'image',
            'updated_at',
            'created_at',
        )
        read_only_fields=(
            'author',
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
    class Meta:
        model = TeamPost
        fields = (
            'id',
            'team',
            'title',
            'description',
            'image',
            'updated_at',
            'created_at',
        )

class TeamPostSummarizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamPost
        fields = (
            'id',
            'image',
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