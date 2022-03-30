from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.db import models

User = get_user_model()


class CustomTemplate(models.Model):
    template = models.FileField(upload_to="template/")
    name = models.CharField(max_length=20, validators=[
        MinLengthValidator(1)
    ])
    thumbnail = CloudinaryField("image", null=True, blank=True)


class Preferences(models.Model):
    hobby = models.CharField(max_length=20, unique=True, validators=[
        MinLengthValidator(1),
    ])


class Receiver(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=20, null=True, blank=True, validators=[
        MinLengthValidator(5),
        MaxLengthValidator(20),
    ])
    last_name = models.CharField(max_length=20, null=True, blank=True, validators=[
        MinLengthValidator(5),
        MaxLengthValidator(20),
    ])
    age = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(100)
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
    screenshot = models.URLField()
    template = models.ForeignKey(CustomTemplate, on_delete=models.DO_NOTHING)
