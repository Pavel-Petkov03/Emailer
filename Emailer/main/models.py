from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

User = get_user_model()





class CustomTemplate(models.Model):
    template = models.FileField(upload_to="templates/")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_global_template = models.BooleanField(default=False)


class Receiver(models.Model):
    name = models.CharField(max_length=20)
    mail = models.EmailField(unique=True)
    additional_data = models.JSONField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Group(models.Model):
    name = models.CharField(max_length=20)
    receivers = models.ManyToManyField(Receiver)


class Email(models.Model):
    SUBJECT_MAX_LENGTH = 30
    SUBJECT_MIN_LENGTH = 5
    TO_MAX_LENGTH = 50
    TO_MIN_VALIDATOR = 10

    subject = models.CharField(
        max_length=SUBJECT_MAX_LENGTH,
        validators=[
            MinLengthValidator(SUBJECT_MIN_LENGTH)
        ])

    receiver = models.ForeignKey(Receiver, on_delete=models.CASCADE)

    context = models.JSONField(null=True, blank=True)
    date = models.DateField(null=True, blank=True)