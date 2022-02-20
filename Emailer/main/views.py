from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from Emailer.main.models import Email

from django.core.mail import send_mail


class SendEmailSerializer(ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"


class SendEmailView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [IsAuthenticated, ]
    serializer_class = SendEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            send_mail(
                *serializer.data
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.data, status=status.HTTP_401_UNAUTHORIZED)

