import json
from json import JSONDecodeError
import requests
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from accounts.jwt import generate_access_token
from accounts.models import User
from accounts.serializers import UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=False)
    def check_nickname(self, request):
        nickname = request.query_params.get('nickname')
        try:
            _nickname = User.objects.get(nickname=nickname)
            return Response(status=status.HTTP_409_CONFLICT)
        except:
            return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def login_kakao(self, request):
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
        user = User.objects.get(social_id=social_id)
        access_token = generate_access_token(user.social_id)
        data['access_token'] = access_token
        data['id'] = user.id
        data['nickname'] = user.nickname
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def signup_kakao(self, request):
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
        user = User.objects.create(social_id=social_id)
        data['access_token'] = generate_access_token(user.social_id)

        return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False)
    def login_google(self, request):
        data = {}
        accessToken = json.loads(request.body)
        access_token = accessToken['access_token']
        user_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
        user_json = user_req.json()
        print(user_json)
        social_id = user_json.get('id')
        error = user_json.get("error")
        if error is not None:
            raise JSONDecodeError(error)
        user = User.objects.get(social_id=social_id)
        access_token = generate_access_token(user.social_id)
        data['access_token'] = access_token
        data['id'] = user.id
        data['nickname'] = user.nickname
        return Response(data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def signup_google(self, request):
        data = {}
        accessToken = json.loads(request.body)
        access_token = accessToken['access_token']
        print(access_token)
        user_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")
        user_json = user_req.json()
        print(user_json)
        social_id = user_json.get('user_id')
        error = user_json.get("error")
        if error is not None:
            raise JSONDecodeError(error)
        user = User.objects.create(social_id=social_id, social_type='Google')
        data['access_token'] = generate_access_token(user.social_id)
        return Response(data, status=status.HTTP_201_CREATED)