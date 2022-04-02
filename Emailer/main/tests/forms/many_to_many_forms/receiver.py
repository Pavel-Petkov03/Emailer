import json
import os
from django.core.files import File as DjangoFile
from django.test import TestCase
from django.urls import reverse
from Emailer.authentication.models import CustomUserModel
from Emailer.main.forms.many_to_many_forms import ReceiverForm
from Emailer.main.models import Preferences, Receiver


class TestReceiverForm(TestCase):
    def setUp(self) -> None:
        user = CustomUserModel.objects.create_user("name", "fewfewf")
        self.client.force_login(user)
        self.user = user
        p = Preferences(hobby="a")
        p.save()


    def test_invalid_age_input(self):
        payload = {
            "email": "elias@abv.bg",
            "first_name": "Pavel12",
            "last_name": "Petkov12",
            "age": -10,
            "preferences": [Preferences.objects.first().id],
        }

        form = ReceiverForm(payload)
        for er in form.errors:
            self.assertEqual(er, form.fields["age"].error)

    def test_save_non_existing_receiver(self):
        payload = {
            "email": "elias@abv.bg",
            "first_name": "Pavel12",
            "last_name": "Petkov12",
            "age": 18,
            "preferences": [Preferences.objects.first().id],
        }
        f = ReceiverForm(payload, user=self.user)
        self.assertTrue(f.is_valid())
        f.save(commit=True)
        current_receiver = Receiver.objects.first()
        self.assertEqual(Receiver.objects.all().__len__(), 1)
        self.assertEqual(current_receiver.email, payload["email"])
        self.assertEqual(current_receiver.first_name, payload["first_name"])
        self.assertEqual(current_receiver.last_name, payload["last_name"])
        self.assertEqual(current_receiver.age, payload["age"])
        self.assertEqual(current_receiver.user, self.user)
        for index, preference in enumerate(current_receiver.preferences.all()):
            self.assertEqual(preference, Preferences.objects.get(id=index + 1))

    def test_save_patch_existing_receiver(self):
        """
        This tests if all previous preferences are deleted and new ones are attached
        """
        all_preferences = Preferences.objects.bulk_create([
            Preferences(hobby="first preference"),
            Preferences(hobby="second preference"),
            Preferences(hobby="Third preference")
        ])
        current_receiver = Receiver(
            email="emaIL@abv.bg",
            first_name="first name",
            last_name="last name",
            age=12,
            user=self.user
        )
        current_receiver.save()
        current_receiver.preferences.add(all_preferences[0])  # first preference add

        patch_payload = {
            "email": current_receiver.email,
            "first_name": 'updated first name',
            "last_name": "updated last name",
            "age": 22,
            "preferences": all_preferences[1:]  # second and third preferences
        }
        form = ReceiverForm(patch_payload, user=self.user)
        self.assertTrue(form.is_valid())
        form.save()

        updated_receiver = Receiver.objects.filter(email=current_receiver.email)[0]
        self.assertEqual(updated_receiver.email, patch_payload["email"])
        self.assertEqual(updated_receiver.first_name, patch_payload["first_name"])
        self.assertEqual(updated_receiver.last_name, patch_payload["last_name"])
        self.assertEqual(updated_receiver.age, patch_payload["age"])
        for index, preference in enumerate(updated_receiver.preferences.all()):
            self.assertEqual(preference, patch_payload["preferences"][index])
