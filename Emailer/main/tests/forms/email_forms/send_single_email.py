import os
from django.core.files import File as DjangoFile
from django.test import TestCase
from django.urls import reverse
from Emailer.authentication.models import CustomUserModel
from Emailer.main.models import Receiver, CustomTemplate, Email

from Emailer.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

DIRNAME = os.path.dirname(__file__)


class TestSendSingleEmail(TestCase):
    TEMPLATE_UNIQUE_NAME = "SOME UNIQUE NAME"

    def setUp(self) -> None:
        user = CustomUserModel.objects.create_user(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        user.email_password = EMAIL_HOST_PASSWORD
        user.save()
        self.client.force_login(user)
        self.user = user
        file = DjangoFile(open(os.path.join(DIRNAME, "../../files/some.html"), "rb"), name="s")
        template = CustomTemplate(template=file, name=self.TEMPLATE_UNIQUE_NAME)
        template.save()

    def test_create_receiver_if_does_not_exists__return_new_receiver(self):
        payload = {
            "subject": "s", "template": self.TEMPLATE_UNIQUE_NAME, "message": "some message", "email": "elias@abv.bg"
        }
        self.client.post(reverse("send-single-email"), data=payload)
        self.assertEqual(Receiver.objects.all().__len__(), 1)
        current_receiver = Receiver.objects.get(email__exact=payload["email"], user__exact=self.user)
        self.assertEqual(current_receiver, Receiver.objects.first())
        self.assertEqual(Email.objects.first().receiver, Receiver.objects.first())

    def test_use_existing_receiver__expected_use_the_same(self):
        email = "elias@abv.bg"

        receiver = Receiver(email=email, user_id=self.user.id)
        receiver.save()

        payload = {
            "subject": "s", "template": self.TEMPLATE_UNIQUE_NAME, "message": "some message", "email": email
        }
        self.client.post(reverse("send-single-email"), data=payload)
        self.assertEqual(receiver, Receiver.objects.first())
        current_email = Email.objects.first()
        self.assertEqual(current_email.receiver, receiver)
        self.assertEqual(current_email.subject, payload["subject"])
        self.assertEqual(current_email.template, CustomTemplate.objects.first())
