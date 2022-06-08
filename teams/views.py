from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from posts.models import TeamPost
from posts.seirlaizers import TeamPostSummarizeSerializer
from teams.models import TeamProfile, Member, TeamFollowRelation
from teams.seirlaizers import TeamProfileSerializer, TeamFollowSerializer, ApplySerializer, MemberSummarizeSerializer, \
    MemberSerializer, MemberprofileSummarizeSerializer


class TeamViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            return TeamProfile.objects.filter(members=user)
        else:
            return TeamProfile.objects.all()

    def get_serializer_class(self):
        if self.action == 'follow':
            return TeamFollowSerializer
        elif self.action == 'apply':
            return ApplySerializer
        elif self.action == 'members':
            return MemberSummarizeSerializer
        else:
            return TeamProfileSerializer

    @action(methods=['post'], detail=True)
    def follow(self, request, pk):
        follow = TeamFollowRelation.objects.filter(team_id=pk, follower=request.user).first()
        if follow:
            follow.delete()
            return Response({'message': 'cancel team follow'}, status=status.HTTP_204_NO_CONTENT)
        elif follow is None:
            TeamFollowRelation.objects.create(team_id=pk, follower=request.user)
            return Response({'message': 'success team follow'}, status=status.HTTP_201_CREATED)
        return Response({'error_message': 'request data error'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def apply(self, request, pk):
        applying = Member.objects.filter(team_id=pk, member=request.user).first()
        if applying:
            return Response({'message': 'applied member'}, status=status.HTTP_409_CONFLICT)
        elif applying is None:
            Member.objects.create(team_id=pk, member=request.user)
            return Response({'message': 'success applying'}, status=status.HTTP_201_CREATED)
        return Response({'error_message': 'request data error'}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='settings/members')
    def settings_members(self, request, pk):
        queryset = Member.objects.filter(team_id=pk, member_type='confirmed')
        serializer = MemberSummarizeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='profile/members')
    def profile_members(self, request, pk):
        print('asdasd')
        queryset = Member.objects.filter(team_id=pk, member_type='confirmed')
        serializer = MemberprofileSummarizeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='pended-members')
    def pended_members(self, request, pk):
        queryset = Member.objects.filter(team_id=pk, member_type='pended')
        serializer = MemberSummarizeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def posts(self, request, pk):
        queryset = TeamPost.objects.filter(team_id=pk)
        serializer = TeamPostSummarizeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MemberAPIView(APIView):
    def get_object(self, pk):
        member = get_object_or_404(Member, pk=pk)
        return member

    def put(self, request, pk):
        member = self.get_object(pk)
        serializer = MemberSerializer(member, data=request.data, context={'request': request, 'pk':pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        member = self.get_object(pk)
        member.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)