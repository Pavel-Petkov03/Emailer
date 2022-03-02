from django.conf import settings
from django import forms
from django.core.exceptions import ValidationError


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "type": "text", "class": 'form-control', "placeholder": "Enter Username"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password", "class": 'form-control', "placeholder": "Enter password"
    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password", "class": 'form-control', "placeholder": "Confirm password"
    }))

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


class LoginForm(forms.ModelForm):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = "__all__"
