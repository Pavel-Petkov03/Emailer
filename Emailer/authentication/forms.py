from django import forms
from django.contrib.auth import get_user_model, authenticate, login
from django.core.exceptions import ValidationError

User = get_user_model()


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

    def clean(self):
        confirm_password_error_message = "password and confirm password must match"
        if self.data["password"] != self.data["confirm_password"]:
            raise ValidationError(confirm_password_error_message)

    def save(self, req):
        self.clean()
        current_user = User.objects.create_user(username=self.cleaned_data["username"],
                                                password=self.cleaned_data["password"])
        current_user.save()
        login(req, current_user)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255, required=True, widget=forms.TextInput(attrs={
        "type": "text", "class": 'form-control', "placeholder": "Enter Username"
    }), label='Username')
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "type": "password", "class": 'form-control', "placeholder": "Enter password"
    }), required=True, label="Password")

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, but username and password does not match")
        return self.cleaned_data

    def login(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
