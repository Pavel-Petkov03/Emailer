import os
from django.core.files import File as DjangoFile
from django.test import TestCase
from django.urls import reverse
from Emailer.authentication.models import CustomUserModel
from Emailer.main.models import  CustomTemplate, Group
DIRNAME = os.path.dirname(__file__)

class TestSendMassEmailView(TestCase):
    TEMPLATE_UNIQUE_NAME = "some name"


    def setUp(self) -> None:
        file = DjangoFile(open(os.path.join(DIRNAME, "../../files/some.html"), "rb"), name="s")
        template = CustomTemplate(template=file, name=self.TEMPLATE_UNIQUE_NAME)
        template.save()
        user = CustomUserModel.objects.create_user("fewfwe", "fewfewfew")
        user.email_password = "fewfwefew"
        user.save()
        self.client.force_login(user)

    def test_success_redirect(self):
        group = Group(name="some name")
        group.save()
        payload = {
            "subject": "s", "template": self.TEMPLATE_UNIQUE_NAME, "message": "some message",
        }
        response = self.client.post(reverse("preview group", args=[group.id]), data=payload)
        self.assertRedirects(response, "/sender/folder")

    def test_template_used(self):
        group = Group(name="some name")
        group.save()
        response = self.client.get(reverse("preview group", args=[group.id]))
        self.assertTemplateUsed(response, "send_mass_email.html")

    def test_form_used(self):
        group = Group(name="some name")
        group.save()
        response = self.client.get(reverse("preview group", args=[group.id]))
        self.assertContains(response, group.name)

