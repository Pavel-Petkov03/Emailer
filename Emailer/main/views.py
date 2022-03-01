from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from Emailer.main.models import  CustomTemplate
from django.core.mail import send_mail
from Emailer.main.serializers import SendEmailSerializer, CreateCustomTemplateSerializer


class EmailView(generics.GenericAPIView, generics.mixins.CreateModelMixin):
    serializer_class = SendEmailSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        template_url = CustomTemplate.objects.get(pk=request.data.template_id)
        request.data.update({"user": request.user.id})
        response = super().create(request, *args, **kwargs)
        create_email(request.data, request.user, template_url)
        return response


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


class CustomTemplateView(generics.GenericAPIView, generics.mixins.DestroyModelMixin,
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
