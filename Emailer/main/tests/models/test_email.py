from django.db import DataError
from django.test import TestCase

from Emailer.authentication.models import CustomUserModel
from Emailer.main.models import  Receiver, CustomTemplate, Email


class TestEmail(TestCase):


    def setUp(self) -> None:
        user = CustomUserModel(email="pavkata@abv.bg")
        user.save()
        receiver = Receiver(email="elias@abv.bg",user=user)
        receiver.save()
        template = CustomTemplate(name="some name")
        template.save()
        self.screenshot = "https://vsetaq.com"
        self.receiver = receiver
        self.template = template

    def test_subject_max_length(self):
        max_length_subject = Email.SUBJECT_MAX_LENGTH
        subject = "s"*max_length_subject
        email = Email(
            screenshot=self.screenshot,
            template=self.template,
            receiver=self.receiver,
            subject=subject
        )
        email.save()
        self.assertEqual(email.subject, subject)

    def test_too_large_name(self):
        too_large_length_subject = Email.SUBJECT_MAX_LENGTH + 1
        subject = "s" * too_large_length_subject
        with self.assertRaises(DataError):
            email = Email(
                screenshot=self.screenshot,
                template=self.template,
                receiver=self.receiver,
                subject=subject
            )
            email.save()
            self.assertEqual(email.subject, subject)

    def test_time_now(self):
        subject = "fewfew"
        email = Email(
            screenshot=self.screenshot,
            template=self.template,
            receiver=self.receiver,
            subject=subject
        )
        email.save()
        from datetime import datetime
        self.assertEqual(email.date.now(), datetime.now())

