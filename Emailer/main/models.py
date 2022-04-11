import cloudinary.uploader
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MinValueValidator, MaxValueValidator, MaxLengthValidator
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
User = get_user_model()

class CustomTemplate(models.Model):
    NAME_MAX_LENGTH = 20
    template = models.FileField(upload_to="templates/email-templates")
    name = models.CharField(max_length=NAME_MAX_LENGTH, validators=[
        MinLengthValidator(1)
    ])
    thumbnail = CloudinaryField("image", null=True, blank=True)


class Preferences(models.Model):
    HOBBY_MAX_LENGTH = 20
    hobby = models.CharField(max_length=20, unique=True, validators=[
        MinLengthValidator(1),
    ])


class Receiver(models.Model):
    FIRST_NAME_MAX_LENGTH = 20
    LAST_NAME_MAX_LENGTH = 20

    email = models.EmailField()
    first_name = models.CharField(max_length=FIRST_NAME_MAX_LENGTH, null=True, blank=True, validators=[
        MinLengthValidator(5),
        MaxLengthValidator(20),
    ])
    last_name = models.CharField(max_length=LAST_NAME_MAX_LENGTH, null=True, blank=True, validators=[
        MinLengthValidator(5),
        MaxLengthValidator(20),
    ])
    age = models.IntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(100)
    ], null=True, blank=True)
    preferences = models.ManyToManyField(Preferences, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Group(models.Model):
    NAME_MAX_LENGTH = 20
    name = models.CharField(max_length=NAME_MAX_LENGTH)
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
    date = models.DateTimeField(auto_now_add=True)
    screenshot = models.URLField()
    template = models.ForeignKey(CustomTemplate, on_delete=models.DO_NOTHING)


@receiver(post_delete, sender=Email)
def delete_cloudinary_image(sender, instance, *args, **kwargs):
    public_id = instance.screenshot.split("/")[-1].split(".")[0]
    cloudinary.uploader.destroy(public_id)
