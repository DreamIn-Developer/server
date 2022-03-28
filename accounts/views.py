import json
from json import JSONDecodeError

import requests
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        accessToken = json.loads(request.body)
        access_token = accessToken['access_token']
        user_req = requests.get(f"https://kapi.kakao.com/v2/user/me",
                                headers={"Authorization": f"Bearer {access_token}"})
        user_json = user_req.json()
        error = user_json.get("error")
        if error is not None:
            raise JSONDecodeError(error)

        return Response(status=status.HTTP_200_OK)