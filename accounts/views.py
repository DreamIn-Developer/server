import json
from json import JSONDecodeError
import requests
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, mixins
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.jwt import generate_access_token
from accounts.models import User, MainCategory, FollowRelation
from accounts.serializers import UserSerializer, SocialLoginSerializer, CategorySerializer

@api_view(["GET"])
def ping(request):
    res = {
        "server": "on"
    }
    return Response(res, status=status.HTTP_200_OK)

class UserViewSet(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
            categories = categories.split(',')
            instance.categories.clear()
            for category in categories:
                instance.categories.add(category)
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def check_nickname(self, request):
        nickname = request.query_params.get('nickname')
        try:
            _nickname = User.objects.get(nickname=nickname)
            res = {
                'message': 'check nickname fail'
            }
            return Response(res, status=status.HTTP_409_CONFLICT)
        except:
            res = {
                'message': 'check nickname ok'
            }
            return Response(res, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False)
    def kakao(self, request):
        data = {}
        accessToken = json.loads(request.body)
        access_token = accessToken['access_token']
        print(access_token)
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
            user = User.objects.create_user(social_id=social_id, social_type='google', email=f'{social_id}@dream.com',nickname='example')
            data['access_token'] = generate_access_token(user.social_id)
            data['id'] = user.id
            data['nickname'] = user.nickname
            data['social_type'] = user.social_type
            return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=False)
    def google(self, request):
        data = {}
        accessToken = json.loads(request.body)
        access_token = accessToken['access_token']
        print(access_token)
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
            user = User.objects.create_user(social_id=social_id, social_type='google', email=f'{social_id}@dream.com', nickname='example')
            data['access_token'] = generate_access_token(user.social_id)
            data['id'] = user.id
            data['nickname'] = user.nickname
            data['social_type'] = user.social_type
            return Response(data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def follow(self, request, pk):
        follow = FollowRelation.objects.filter(follower=request.user, following_id=pk).first()
        if follow:
            follow.delete()
            return Response({'message': "cancel follow"},status=status.HTTP_204_NO_CONTENT)
        elif follow is None:
            FollowRelation.objects.create(follower=request.user, following_id=pk)
            return Response({'message': 'success follow'}, status=status.HTTP_201_CREATED)
        return Response({'error_message': 'request data error'}, status=status.HTTP_400_BAD_REQUEST)

class CategoryAPIView(mixins.ListModelMixin,GenericViewSet):
    queryset = MainCategory.objects.all()
    serializer_class = CategorySerializer
    pagination_class = None
