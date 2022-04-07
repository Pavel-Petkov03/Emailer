from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import DataError
from django.test import TestCase

from Emailer.main.models import CustomTemplate


class TestTemplate(TestCase):

    def setUp(self) -> None:
        self.file = SimpleUploadedFile("random.html", "", content_type="text/html")

    def test_maximum_name_length(self):
        name_max_length = CustomTemplate.NAME_MAX_LENGTH
        name_max = "s" * name_max_length
        template = CustomTemplate(name=name_max, template=self.file)
        template.save()
        self.assertEqual(template.name, name_max)

    def test_too_large_name_expected_error(self):
        name_too_large_length = CustomTemplate.NAME_MAX_LENGTH + 1
        name_max = "s" * name_too_large_length
        template = CustomTemplate(name=name_max, template=self.file)
        with self.assertRaises(DataError):
            template.save()
