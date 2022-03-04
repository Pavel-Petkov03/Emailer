from django.conf import settings
from django.contrib.auth import get_user_model
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

    receiver = models.CharField(max_length=TO_MAX_LENGTH, validators=[
        MinLengthValidator(TO_MIN_VALIDATOR)
    ])

    context = models.JSONField(null=True, blank=True)

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="map")

    date = models.DateField()




class CustomTemplate(models.Model):
    template = models.FileField(upload_to="templates/")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_global_template = models.BooleanField(default=False)
