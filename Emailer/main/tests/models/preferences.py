from django.db import IntegrityError, DataError
from django.test import TestCase

from Emailer.main.models import Preferences


class TestPreferences(TestCase):

    def test_hobby_name_min_length(self):
        min_hobby_length = 1
        hobby = "s" * min_hobby_length
        preference = Preferences(hobby=hobby)
        preference.save()
        self.assertEqual(preference.hobby, hobby)

    def test_hobby_name_max_length(self):
        max_hobby_length = 20
        hobby = "s" * max_hobby_length
        preference = Preferences(hobby=hobby)
        preference.save()
        self.assertEqual(preference.hobby, hobby)

    def test_hobby_name_above_max_length__expected_error(self):
        with self.assertRaises(DataError):
            too_large_hobby_name_length = 21
            hobby = "s" * too_large_hobby_name_length
            preference = Preferences(hobby=hobby)
            preference.save()
            self.assertEqual(preference.hobby, hobby)

    def test_hobby_unique(self):
        with self.assertRaises(IntegrityError) as error:
            hobby_not_unique = "not unique hobby"
            creation_array = [Preferences(hobby=hobby_not_unique), Preferences(hobby=hobby_not_unique)]
            Preferences.objects.bulk_create(creation_array)




