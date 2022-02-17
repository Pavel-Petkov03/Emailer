from django.urls import path
from rest_framework import serializers
from rest_framework_simplejwt import views
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from Emailer.authentication.views import RegisterAPIView

urlpatterns = [
    path("login", views.TokenObtainPairView.as_view()),
    path("refresh", views.TokenRefreshView.as_view()),
    path("register", RegisterAPIView.as_view()),
]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        if not attrs["username"]:
            pass
#
#
#
class CustomTokenObtainView(views.TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
