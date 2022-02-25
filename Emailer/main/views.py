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


class SendEmailView(generics.GenericAPIView, generics.mixins.CreateModelMixin):
    serializer_class = SendEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        template_url = CustomTemplate.objects.get(pk=request.data.template_id)
        request.data.update({"user": request.user.id})
        response = super().create(request, *args, **kwargs)
        create_email(request.data, request.user, template_url)
        return response

    # def post(self, request):
    #     data = request.data
    #     data["user"] = request.user.id
    #     serializer = self.serializer_class(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         create_email(request.data, request.user, self.__template_url)
    #         return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def create_email(data, user, template_url):
    context = data.context if data.get("context") else {}
    html_message = render_to_string(template_url, {"context": context})
    plain_message = strip_tags(html_message)
    send_mail(
        data["subject"],
        plain_message,
        user.email,
        (data["to"],),
        html_message=html_message
    )


class CreateCustomTemplate(generics.GenericAPIView, generics.mixins.DestroyModelMixin,
                           generics.mixins.CreateModelMixin,
                           generics.mixins.ListModelMixin):
    serializer_class = CreateCustomTemplateSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        current_user_id = request.user.id
        if request.user.is_staff:
            is_global_template = True
        else:
            is_global_template = False
        request.data.update({"user": current_user_id, "is_global_template": is_global_template})
        return super().create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return self.serializer_class.Meta.model.objects. \
            filter(is_global_template=self.kwargs["is_global_template"]) \
            # .order_by(self.kwargs["filter"])
