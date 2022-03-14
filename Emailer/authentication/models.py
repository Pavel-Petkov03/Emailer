from django.contrib.auth.models import AbstractUser
from django.db import models
from Emailer.authentication.base_manager import UserManager


class CustomUserModel(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
