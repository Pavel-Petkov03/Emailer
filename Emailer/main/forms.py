from django.contrib.auth.models import User
from django import forms


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password", "confirm_password")
        widgets = {
            "username": forms.TextInput(attrs={
                "type": "text", "class": 'form-control', "placeholder": "Enter Username"
            }),
            "password": forms.PasswordInput(attrs={
                "type": "password", "class": 'form-control', "placeholder": "Enter password"
            }),
            "confirm_password": forms.PasswordInput(attrs={
                "type": "password", "class": 'form-control', "placeholder": "Confirm password"
            }),
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "password")
