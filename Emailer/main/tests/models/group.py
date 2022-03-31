from django.db import DataError
from django.test import TestCase
from Emailer.main.models import Group



class TestGroup(TestCase):

    def test_name_max_length(self):
        name_max_length = Group.NAME_MAX_LENGTH
        name = "s"* name_max_length
        group = Group(
            name=name
        )
        group.save()
        self.assertEqual(name, group.name)


    def test_name_t00_large__expected_error(self):
        name_max_length = Group.NAME_MAX_LENGTH + 1
        name = "s" * name_max_length
        with self.assertRaises(DataError):
            group = Group(
                name=name
            )
            group.save()