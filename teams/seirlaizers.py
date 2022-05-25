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
            'user',
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
    class Meta:
        model = Member
        fields = (
            'user',
            'nickname',
            'post_count',
            'image',
            'member_type',
            'category',
            'following_count',
            'follower_count',
        )
        read_only_fields = (
            'id',
            'nickname',
            'post_count',
            'image',
        )