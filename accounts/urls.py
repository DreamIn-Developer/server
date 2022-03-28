from django.urls import path

from accounts.views import LoginView

urlpatterns = [
    path('login/kakao', LoginView.as_view())
]