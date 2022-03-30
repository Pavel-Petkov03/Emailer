from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from Emailer.main.models import CustomTemplate


class TestTemplate(TestCase):


    def setUp(self) -> None:
        self.file = SimpleUploadedFile("random.html", "", content_type="text/html")

    def test_minimum_name(self):
        name_min_length = 1
        name_min = "s" * name_min_length
        template = CustomTemplate(name=name_min, template=self.file)
        template.save()
        self.assertEqual(template.name, name_min)

    def test_maximum_name_length(self):
        name_max_length = 20
        name_max = "s"*name_max_length
        template = CustomTemplate(name=name_max, template=self.file)
        template.save()
        self.assertEqual(template.name, name_max)


    def test_too_large_name_expected_error(self):
        name_too_large_length = 21
        name_max = "s" * name_too_large_length
        template = CustomTemplate(name=name_max, template=self.file)
        template.save()
        self.assertEqual(template.name, name_max)
