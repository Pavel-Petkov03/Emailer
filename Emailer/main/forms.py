from django.contrib.auth.models import User
from django import forms


class CustomAuthForm(forms.ModelForm):
    class Meta:
        abstract = True


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("username" , "password", "confirm_password")
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

# <form class="custom-form">
#                <h3>Sign In</h3>
#                <div class="form-group">
#                    <label>Enter Username</label>
#                    <input type="email" class="form-control" placeholder="Enter username"/>
#                </div>
#
#                <div class="form-group">
#                    <label>Password</label>
#                    <input type="password" class="form-control" placeholder="Enter password"/>
#                </div>
#                <button type="submit" class="btn btn-primary btn-block">Submit</button>
#                <p class="forgot-password text-right">
#                    Forgot <a href="#">password?</a>
#                </p>
#            </form>
