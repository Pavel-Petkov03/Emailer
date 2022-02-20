from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.views import APIView

from Emailer.main.models import Email

from django.core.mail import send_mail


class SendEmailSerializer(ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"


class SendEmailView(APIView):
    serializer_class = SendEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_email(request.data, request.user)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


def create_email(data, user):
    send_mail(
        data["subject"],
        data["message"],
        user.email,
        (data["to"],)
    )
