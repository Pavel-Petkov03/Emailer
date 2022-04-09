from django.core.exceptions import ValidationError


def is_gmail_validator(email : str):
    gmail_pattern = "@gmail.com"
    if not email.endswith(gmail_pattern):
        raise ValidationError("The provided email must be gmail")