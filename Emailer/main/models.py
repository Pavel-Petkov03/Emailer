import os
import string
from random import choice

from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

User = get_user_model()



class CustomTemplate(models.Model):
    template = models.FileField(upload_to="template/")
    name = models.CharField(max_length=20)


class Preferences(models.Model):
    hobby = models.CharField(max_length=20, unique=True)


class Receiver(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    age = models.IntegerField(validators=[
        MinValueValidator(0)
    ], null=True, blank=True)
    preferences = models.ManyToManyField(Preferences, max_length=20, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=20)
    receivers = models.ManyToManyField(Receiver)


class Email(models.Model):
    SUBJECT_MAX_LENGTH = 30
    SUBJECT_MIN_LENGTH = 5

    subject = models.CharField(
        max_length=SUBJECT_MAX_LENGTH,
        validators=[
            MinLengthValidator(SUBJECT_MIN_LENGTH)
        ])

    receiver = models.ForeignKey(Receiver, on_delete=models.DO_NOTHING, related_name="receiver")
    is_deleted = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    screenshot = CloudinaryField("image", folder="Emailer")
    template = models.ForeignKey(CustomTemplate, on_delete=models.DO_NOTHING)



