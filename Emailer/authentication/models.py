from django.contrib.auth.models import AbstractUser
from django.db import models
from Emailer.authentication.base_manager import UserManager
from Emailer.authentication.validators import is_gmail_validator


class CustomUserModel(AbstractUser):
    username = None
    email = models.EmailField(unique=True, validators=[is_gmail_validator])
    email_password = models.CharField(max_length=30, null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
        unique_together = ("email", )
        db_table = "User"

