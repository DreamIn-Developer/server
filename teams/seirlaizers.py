from rest_framework import serializers
from teams.models import Member, TeamProfile, TeamFollowRelation


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
    def update(self, validated_data):
        validated_data["member"] = self.context.get("request").user
        return super().update(validated_data)

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

class TeamProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamProfile
        fields = (
            'id',
            'title',
            'description',
            'leader',
            'image',
            'post_count',
            'member_count',
            'team_follow_count',
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


class MemberSummarizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = (
            'id',
            'nickname',
            'post_count',
            'image',
            'member_type',
        )
        read_only_fields = (
            'id',
            'nickname',
            'post_count',
            'image',
        )