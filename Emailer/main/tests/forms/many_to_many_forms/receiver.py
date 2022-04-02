import os
from django.core.files import File as DjangoFile
from django.test import TestCase
from django.urls import reverse
from Emailer.authentication.models import CustomUserModel
from Emailer.main.models import Preferences


class TestReceiverForm(TestCase):
    def setUp(self) -> None:
        user = CustomUserModel.objects.create_user("name", "fewfewf")
        self.client.force_login(user)
        Preferences.objects.bulk_create(
            [
                Preferences(hobby="a"),
                Preferences(hobby="b")
            ]
        )

    def test_save_non_existing_receiver(self):
        payload = {
            "email": "elias@abv.bg",
            "first_name": "Pavel12",
            "last_name": "Petkov12",
            "age": 18,
            "preferences": ['a'],
        }
        response = self.client.post(reverse("add receiver"), payload)
        print(1)
