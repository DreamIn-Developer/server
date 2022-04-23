import json
from json import JSONDecodeError
import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from accounts.jwt import generate_access_token
from accounts.models import User, Category
from accounts.serializers import UserSerializer, FollowSerializer, SocialLoginSerializer, CategorySerializer


class UserViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,GenericViewSet):
    queryset = User.objects.all()
    def get_serializer_class(self):
        if self.action == 'follow':
            return FollowSerializer
        else:
            return UserSerializer

    @swagger_auto_schema(operation_summary="메인 페이지(유저 리스트)", operation_description='메인 페이지의 컨텐츠로 이용될 유저 리스트입니다.')
    def list(self,request,*args, **kwargs):
        return super().list(request,*args, **kwargs)

    @swagger_auto_schema(operation_summary="개인 프로필 조회")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(operation_summary="개인 프로필 수정 및 회원가입 폼 저장", operation_description='1차적으로 회원가입은 서버에 유효한 토큰을 보냈을때 가입되며 이후 회원가입폼 정보를 입력하게되면 저장할때 쓰이는 api입니다. 또한 추후 자신의 프로필정보를 수정할때도 이용됩니다.')
    def update(self, request, *args, **kwargs):
        categories = request.data.get('categories', None)
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        if categories:
            for category in categories:
                instance.categories.add(category)
        return Response(serializer.data)

    @swagger_auto_schema(operation_summary="닉네임 중복체크",operation_description="/api/users/check_nickname?nickname=~~와 같이 요청해주면 됩니당~")
    @action(methods=['get'], detail=False)
    def check_nickname(self, request):
        nickname = request.query_params.get('nickname')
        try:
            _nickname = User.objects.get(nickname=nickname)
            return Response(status=status.HTTP_409_CONFLICT)
        except:
            return Response(status=status.HTTP_200_OK)

    @swagger_auto_schema(operation_summary="카카오 소셜로그인",request_body=SocialLoginSerializer)
    @action(methods=['post'], detail=False)
    def kakao(self, request):
        data = {}
        accessToken = json.loads(request.body)
        access_token = accessToken['access_token']
        user_req = requests.get(f"https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"})
        user_json = user_req.json()
        social_id = user_json.get('id')
        error = user_json.get("error")
        if error is not None:
            raise JSONDecodeError(error)
        try:
            user = User.objects.get(social_id=social_id)
            if user is None:
                raise Exception
            access_token = generate_access_token(user.social_id)
            data['access_token'] = access_token
            data['id'] = user.id
            data['nickname'] = user.nickname
            data['social_type'] = user.social_type
            return Response(data, status=status.HTTP_200_OK)

        except:
            user = User.objects.create(social_id=social_id, social_type='google')
            data['access_token'] = generate_access_token(user.social_id)
            data['id'] = user.id
            data['nickname'] = user.nickname
            data['social_type'] = user.social_type
            return Response(data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_summary="구글 소셜로그인", request_body=SocialLoginSerializer)
    @action(methods=['post'], detail=False)
    def google(self, request):
        data = {}
        accessToken = json.loads(request.body)
        access_token = accessToken['access_token']
        user_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
        user_json = user_req.json()
        social_id = user_json.get('user_id')
        error = user_json.get("error")
        if error is not None:
            raise JSONDecodeError(error)
        try:
            user = User.objects.get(social_id=social_id)
            if user is None:
                raise Exception
            access_token = generate_access_token(user.social_id)
            data['access_token'] = access_token
            data['id'] = user.id
            data['nickname'] = user.nickname
            data['social_type'] = user.social_type
            return Response(data, status=status.HTTP_200_OK)

        except:
            user = User.objects.create(social_id=social_id, social_type='google')
            data['access_token'] = generate_access_token(user.social_id)
            data['id'] = user.id
            data['nickname'] = user.nickname
            data['social_type'] = user.social_type
            return Response(data, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(operation_summary="유저 팔로우", operation_description='헤더의 토큰값을 필수로 넣어주세요')
    @action(methods=['post'], detail=True)
    def follow(self, request, pk):
        serializer = FollowSerializer(data=request.data, context={'request':request, 'pk':pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListAPIView(mixins.ListModelMixin,GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer