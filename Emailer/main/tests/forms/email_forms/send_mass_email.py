import os
from django.core.files import File as DjangoFile
from django.test import TestCase
from django.urls import reverse
from Emailer.authentication.models import CustomUserModel
from Emailer.main.models import Receiver, CustomTemplate, Email, Group

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

    def test_send_mass_mail_create_all_emails_and_attach_receivers(self):
        group = Group(name="some name")
        group.save()
        receiver_list = [
            Receiver(email="a@abv.bg", user_id=self.user.id),
            Receiver(email="b@abv.bg", user_id=self.user.id),
            Receiver(email="v@abv.bg", user_id=self.user.id),
        ]
        Receiver.objects.bulk_create(receiver_list)
        group.receivers.add(*receiver_list)
        group.save()

        payload = {
            "subject": "s", "template": self.TEMPLATE_UNIQUE_NAME, "message": "some message"
        }
        self.client.post(reverse("preview group", args=[group.id]), data=payload)
        self.assertEqual(Email.objects.all().__len__(), 3)
        for index, email in enumerate(Email.objects.all()):
            self.assertEqual(receiver_list[index], email.receiver)