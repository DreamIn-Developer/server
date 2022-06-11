from rest_framework import serializers
from teams.models import Member, TeamProfile, TeamFollowRelation

# 이미 지원했을때를 고려해야함
class ApplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = (
            'team',
            'member',
        )
        read_only_fields = (
            'team',
            'member',
        )

    def create(self, validated_data):
        validated_data["member"] = self.context.get("request").user
        validated_data["team_id"] = self.context.get("pk")
        return super().create(validated_data)

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = (
            'id',
            'team',
            'member',
            'member_type',
        )
        read_only_fields = (
            'id',
            'team',
            'member',
            'member_type',
        )

    def update(self,instance, validated_data):
        validated_data["member_type"] = 'confirmed'
        return super().update(instance,validated_data)

# 이미 팔로우하고 있을때를 구별해야함
class TeamFollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamFollowRelation
        fields = (
            'follower',
            'team',
        )
        read_only_fields = (
            'follower',
            'team',
        )

    def create(self, validated_data):
        validated_data["follower"] = self.context.get("request").user
        validated_data["team_id"] = self.context.get("pk")
        return super().create(validated_data)

class ApplyCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = (
            'member',
            'member_type',
        )

class TeamProfileSerializer(serializers.ModelSerializer):
    check_applied = serializers.SerializerMethodField()

    class Meta:
        model = TeamProfile
        fields = (
            'id',
            'title',
            'description',
            'leader',
            'team_profile_image',
            'background_image',
            'post_count',
            'member_count',
            'team_follow_count',
            'check_applied',
        )
        read_only_fields=(
            'leader',
            'post_count',
            'member_count',
            'team_follow_count',
        )

    def create(self, validated_data):
        validated_data["leader"] = self.context.get("request").user
        return super().create(validated_data)

    def get_check_applied(self,obj):
        member = Member.objects.filter(team=obj)
        serializer = ApplyCheckSerializer(member, many=True)
        return serializer.data

class MemberSummarizeSerializer(serializers.ModelSerializer):
    member_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields = (
            'member_id',
            'user_id',
            'nickname',
            'post_count',
            'image',
            'member_type',
            'main_category',
            'following_count',
            'follower_count',
        )
        read_only_fields = (
            'id',
            'nickname',
            'post_count',
            'image',
        )

    def get_user_id(self,obj):
        return obj.member.id

    def get_member_id(self,obj):
        return obj.id

class MemberprofileSummarizeSerializer(serializers.ModelSerializer):
    member_id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    class Meta:
        model = Member
        fields = (
            'member_id',
            'user_id',
            'nickname',
            'post_count',
            'image',
            'member_type',
            'sub_category',
            'following_count',
            'follower_count',
        )
        read_only_fields = (
            'id',
            'nickname',
            'post_count',
            'image',
        )

    def get_user_id(self,obj):
        return obj.member.id

    def get_member_id(self,obj):
        return obj.id