from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models


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
    message = models.TextField()

    to = models.CharField(max_length=TO_MAX_LENGTH, validators=[
        MinLengthValidator(TO_MIN_VALIDATOR)
    ])

    upload_image = models.ImageField(null=True, blank=True,
    validators=())

    user = models.ForeignKey(User, on_delete=models.CASCADE)
