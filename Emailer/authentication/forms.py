from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ValidationError

from Emailer.authentication.models import CustomUserModel

User = get_user_model()


class RegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        "type": "text", "class": 'form-control', "placeholder": "Enter mail"
    }), label='Mail')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password", "class": 'form-control', "placeholder": "Enter password"
    }), label='Password')

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password", "class": 'form-control', "placeholder": "Confirm password"
    }), label='Confirm Password')

    def clean(self):
        confirm_password_error_message = "password and confirm password must match"
        if self.data["password"] != self.data["confirm_password"]:
            raise ValidationError(confirm_password_error_message)

    def save(self):
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        User.objects.create_user(email=email, password=password)

    class Meta:
        fields = ("email", "password", "confirm_password")
        model = User


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, required=True, widget=forms.EmailInput(attrs={
        "type": "text", "class": 'form-control', "placeholder": "Enter Mail"
    }), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password", "class": 'form-control', "placeholder": "Enter password"
    }), required=True, label="Password")

    def clean(self):
        email = self.data["email"]
        password = self.data["password"]
        user = authenticate(email=email, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, but email and password does not match")
        return self.cleaned_data

    def login(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        return user


class EditProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = CustomUserModel
        fields = ("first_name", "last_name", "email_password")
        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Enter First Name"
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Enter Last Name"
            }),
            "email_password": forms.PasswordInput(attrs={
                "placeholder": "Enter Email Password"
            }),
        }
