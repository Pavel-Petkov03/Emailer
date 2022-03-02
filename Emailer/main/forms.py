from django.conf import settings
from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.forms import ModelForm


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text", "class": 'form-control', "placeholder": "Enter Username"
    }), label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password", "class": 'form-control', "placeholder": "Enter password"
    }), label='Password')

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password", "class": 'form-control', "placeholder": "Confirm password"
    }), label='Confirm Password')

    def save(self):
        self.clean()
        self.full_clean()
        confirm_password_error_message = "password and confirm password must match"
        if self.fields["password"] != self.fields["confirm_password"]:
            raise ValidationError(confirm_password_error_message)
        payload = {
            "username": self.fields["username"],
            "password": self.fields["password"],
        }
        instance = settings.AUTH_USER_MODEL(payload).save()
        return instance


class LoginForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text", "class": 'form-control', "placeholder": "Enter Username"
    }), label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password", "class": 'form-control', "placeholder": "Enter password"
    }), label='Password')

    class Meta:
        model = get_user_model()
        fields = ("username", "password")
