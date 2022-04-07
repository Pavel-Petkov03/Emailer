import os
from django.core.files import File as DjangoFile
from django.test import TestCase
from django.urls import reverse
from Emailer.authentication.models import CustomUserModel
from Emailer.main.models import CustomTemplate

DIRNAME = os.path.dirname(__file__)


class TestSingleEmailView(TestCase):
    TEMPLATE_UNIQUE_NAME = "some name"

    def setUp(self) -> None:
        file = DjangoFile(open(os.path.join(DIRNAME, "../../files/some.html"), "rb"), name="s")
        template = CustomTemplate(template=file, name=self.TEMPLATE_UNIQUE_NAME)
        template.save()
        self.template = template
        user = CustomUserModel.objects.create_user("fewfwe", "fewfewfew")
        user.email_password = "fewfwefew"
        user.save()
        self.client.force_login(user)

    def test_template_used(self):
        response = self.client.get(reverse("send-single-email"))
        self.assertTemplateUsed(response, "send-single-email.html")

    def test_success_redirect(self):
        payload = {"message": "1", "subject": "1", "email": "elias@abv.bg", "template" : self.template.name}
        response = self.client.post(reverse("send-single-email"), payload)
        self.assertRedirects(response, "/sender/folder")
