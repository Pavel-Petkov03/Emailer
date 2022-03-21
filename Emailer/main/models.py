import os
import string
from random import choice
from django.contrib.auth import get_user_model
from django.core.files import File
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
    date = models.DateTimeField(auto_now=True)
    screenshot = models.ImageField(null=True, blank=True, upload_to="screenshots/")
    template = models.ForeignKey(CustomTemplate, on_delete=models.DO_NOTHING)

    def save(self, *args, **kwargs):
        """
        The name of the saved file will be combination if :
            - sender id
            - receiver id
            - random generated code
        """
        path = self.screenshot.path
        with open(path, "rb") as file:
            self.screenshot.save(self.__generate_file_location(), File(file), save=False)
        os.remove(path)
        super().save(*args, **kwargs)

    def __generate_file_location(self):
        receiver_id = self.receiver.id
        sender_id = self.receiver.user.id
        png_extension = ".png"
        return f'{sender_id}-{receiver_id}-{self.__generate_random_id()}{png_extension}'

    @staticmethod
    def __generate_random_id():
        n = 10
        return ''.join(choice(string.ascii_uppercase + string.digits) for _ in range(n))