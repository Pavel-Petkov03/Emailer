from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from Emailer.main.models import Email

from django.core.mail import send_mail


class SendEmailSerializer(ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"


class SendEmailView(APIView):
    serializer_class = SendEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            send_mail(
                request["subject"],
                request["message"],
                self.user.email,
                [request["to"]]
            )
