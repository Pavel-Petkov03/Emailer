from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

User = get_user_model()


class CustomTemplate(models.Model):
    template = models.FileField(upload_to="template/")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_global_template = models.BooleanField(default=False)


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
    date = models.DateField(null=True, blank=True)
    template = models.ForeignKey(CustomTemplate, on_delete=models.DO_NOTHING, null=True, blank=True)
    screenshot = models.ImageField(null=True, blank=True, upload_to="screenshots/")
