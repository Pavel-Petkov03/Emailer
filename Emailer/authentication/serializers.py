from rest_framework import serializers
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "last_name", "email", "password",)
        model = User


class LoginSerializer(serializers.ModelSerializer):


    class Meta:
        fields = ("email", "password")
        model = User
