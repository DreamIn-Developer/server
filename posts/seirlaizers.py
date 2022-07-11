from rest_framework import serializers

from images.models import Image
from posts.models import Post, Comment, BookMark, TeamPost, TeamComment, PostLike, TeamPostLike, TeamBookMark


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = (
            'image',
        )

class PostRetrieveSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    is_like = serializers.SerializerMethodField(read_only=True)
    is_scrap = serializers.SerializerMethodField(read_only=True)
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
            'is_like',
            'is_scrap',
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
    def get_is_like(self, obj):
        user = self.context.get("request").user
        if user != None:
            is_like = PostLike.objects.filter(user_id=user.id, post=obj).first()
            if is_like is None:
                return False
            else:
                return True
        else:
            return False

    def get_is_scrap(self, obj):
        user = self.context.get("request").user
        if user != None:
            is_scrap = BookMark.objects.filter(user_id=user.id, post=obj).first()
            if is_scrap is None:
                return False
            else:
                return True
        else:
            return False


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
            'image_list',
        )

class PostSummarizeSerializer(serializers.ModelSerializer):
    images = ImageSerializer(read_only=True, many=True)
    is_like = serializers.SerializerMethodField()
    is_scrap = serializers.SerializerMethodField()
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
            'like_count',
            'scrap_count',
            'is_like',
            'is_scrap',
        )
        read_only_fields=(
            'comment_count',
            'like_count',
            'scrap_count',
            'is_like',
            'is_scrap',
        )
    def get_is_like(self, obj):
        user = self.context.get("request").user
        if user != None:
            is_like = PostLike.objects.filter(user_id=user.id, post=obj).first()
            if is_like is None:
                return False
            else:
                return True
        else:
            return False

    def get_is_scrap(self, obj):
        user = self.context.get("request").user
        if user != None:
            is_scrap = BookMark.objects.filter(user_id=user.id, post=obj).first()
            if is_scrap is None:
                return False
            else:
                return True
        else:
            return False

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
    is_like = serializers.SerializerMethodField()
    is_scrap = serializers.SerializerMethodField()
    class Meta:
        model = TeamPost
        fields = (
            'id',
            'team',
            'images',
            'title',
            'created_at',
            'updated_at',
            'comment_count',
            'like_count',
            'scrap_count',
            'is_like',
            'is_scrap'
        )
    def get_is_like(self, obj):
        user = self.context.get("request").user
        if user != None:
            is_like = TeamPostLike.objects.filter(user_id=user.id, team_post=obj).first()
            if is_like is None:
                return False
            else:
                return True
        else:
            return False

    def get_is_scrap(self, obj):
        user = self.context.get("request").user
        if user != None:
            is_scrap = TeamBookMark.objects.filter(user_id=user.id, post=obj).first()
            if is_scrap is None:
                return False
            else:
                return True
        else:
            return False

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