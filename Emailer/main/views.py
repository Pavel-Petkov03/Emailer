from django.contrib.auth.models import User
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import strip_tags
# Create your views here.
from rest_framework import status, generics, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer, ModelSerializer
from rest_framework.views import APIView

from Emailer.main.models import Email, CustomTemplate

from django.core.mail import send_mail

from Emailer.main.serializers import SendEmailSerializer, CreateCustomTemplateSerializer


class SendEmailView(APIView):
    serializer_class = SendEmailSerializer
    permission_classes = [IsAuthenticated]
    __template_url = ""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.template_name = ""

    @property
    def template_name(self):
        return self.__template_name

    @template_name.setter
    def template_name(self, value):
        self.__template_name = value

    def post(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            create_email(request.data, request.user, self.__template_url)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_email(data, user, template_url):
    html_message = render_to_string("s.html", {"context": "context"})
    plain_message = strip_tags(html_message)
    send_mail(
        data["subject"],
        plain_message,
        user.email,
        (data["to"],),
        html_message=html_message
    )


class CreateCustomTemplate(APIView):
    serializer_class = CreateCustomTemplateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        :return: Response with data if created entry else bad request response with errors
        this function checks if user is allowed in admin panel and allows him to post global templates
        """
        data = request.data
        data["user"] = request.user.id
        if request.user.is_staff:
            data["is_global_template"] = True
        else:
            data["is_global_template"] = False
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = CustomTemplate.objects.get(id=pk)
        instance.delete()
