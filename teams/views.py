from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.decorators import action
from teams.models import TeamProfile, Member
from teams.seirlaizers import TeamProfileSerializer, TeamFollowSerializer, ApplySerializer, MemberSummarizeSerializer


class TeamViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        user = self.request.user
        if self.action == 'list':
            return TeamProfile.objects.filter(members=user)
        else:
            TeamProfile.objects.all()

    def get_serializer_class(self):
        if self.action == 'follow':
            return TeamFollowSerializer
        elif self.action == 'apply':
            return ApplySerializer
        elif self.action == 'members':
            return MemberSummarizeSerializer
        else:
            return TeamProfileSerializer

    @swagger_auto_schema(operation_summary="팀프로필 리스트 조회", operation_description='자신이 속해있는 팀프로필 리스트 조회 api입니다. 헤더토큰 필수!')
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="팀프로필 삭제")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="팀프로필 조회", operation_description='해당 id값의 팀프로필 조회 api입니다.')
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="팀프로필 생성", operation_description='헤더 토큰 필수!')
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="팀프로필 수정",
                         operation_description='팀 프로필 수정 api입니다. 헤더 토큰 필수! 팀에 속한 유저만 수정가능합니다.')
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


    @swagger_auto_schema(operation_summary="팀 즐겨찾기", operation_description='자신의 즐겨찾기에 추가하길 원하는 팀프로필 추가 api입니다. 헤더에 토큰 필수!')
    @action(methods=['post'], detail=True)
    def follow(self, request, pk):
        serializer = TeamFollowSerializer(data=request.data, context={'request': request, 'pk': pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="가입 신청", operation_description='자신이 원하는 팀에 지원 하는 api입니다. 헤더에 토큰 필수!')
    @action(methods=['post'], detail=True)
    def apply(self, request, pk):
        serializer = ApplySerializer(data=request.data, context={'request': request, 'pk': pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(operation_summary="팀원 조회", operation_description='해당 팀의 속해있는 멤버를 보는 api입니다.')
    @action(methods=['get'], detail=True)
    def members(self, request, pk):
        queryset = Member.objects.filter(team_id = pk, member_type='confirmed')
        serializer = MemberSummarizeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="가입 신청한 유저 목록 확인", operation_description='본인이 속한 팀에 지원한 유저를 확인하는 api입니다. header에 토큰값 필수!')
    @action(methods=['get'], detail=True)
    def pended_members(self, request, pk):
        queryset = Member.objects.filter(team_id=pk, member_type='pended')
        serializer = MemberSummarizeSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

