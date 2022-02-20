from rest_framework.serializers import ModelSerializer

from Emailer.main.models import Email, CustomTemplate


class SendEmailSerializer(ModelSerializer):
    class Meta:
        model = Email
        fields = "__all__"


class CreateCustomTemplateSerializer(ModelSerializer):
    class Meta:
        model = CustomTemplate
        fields = "__all__"


