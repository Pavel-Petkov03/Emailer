import django.views.generic
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegistrationSerializer
from rest_framework import generics


class SessionCsrfExemptAuthentication(SessionAuthentication):
    def enforce_csrf(self, request):
        pass


class RegisterAPIView(generics.GenericAPIView, generics.mixins.CreateModelMixin):
    authentication_classes = (SessionCsrfExemptAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)


