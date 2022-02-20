from django.contrib.auth.models import User
from django.db.migrations import serializer
from django.shortcuts import render

# Create your views here.
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from Emailer.main.models import Email


class SendEmailSerializer(ModelSerializer):



    class Meta:
        model = Email
        fields = "__all__"


class SendEmailView(APIView):
    serializer_class = SendEmailSerializer
