from django.db import DataError
from django.test import TestCase

from Emailer.authentication.models import CustomUserModel
from Emailer.main.models import Receiver


class TestReceiver(TestCase):

    def setUp(self) -> None:
        self.user = user = CustomUserModel(
            email="elias@abv.bg"
        )
        user.save()

    def test_first_name_max_length(self):
        first_name_max_length = Receiver.FIRST_NAME_MAX_LENGTH
        first_name = "s" * first_name_max_length
        receiver = Receiver(
            first_name=first_name,
            user=self.user
        )

        receiver.save()
        self.assertEqual(first_name, receiver.first_name)

    def test_first_name_too_large__expected_error(self):
        first_name_too_large_length = Receiver.FIRST_NAME_MAX_LENGTH + 1
        first_name = "s" * first_name_too_large_length
        with self.assertRaises(DataError):
            receiver = Receiver(
                first_name=first_name,
                user=self.user
            )

            receiver.save()
            self.assertEqual(first_name, receiver.first_name)

    def test_last_name_max_length(self):
        last_name_max_length = Receiver.LAST_NAME_MAX_LENGTH
        last_name = "s" * last_name_max_length
        receiver = Receiver(
            last_name=last_name,
            user=self.user
        )

        receiver.save()
        self.assertEqual(last_name, receiver.last_name)

    def test_last_name_too_large__expected_error(self):
        last_name_too_large_length = Receiver.LAST_NAME_MAX_LENGTH + 1
        last_name = "s" * last_name_too_large_length
        with self.assertRaises(DataError):
            receiver = Receiver(
                last_name=last_name,
                user=self.user
            )

            receiver.save()
            self.assertEqual(last_name, receiver.first_name)
