from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APITestCase
User = get_user_model()

class TestGenericFolder(APITestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(email="elias@gmail.com", password="1234567")
        self.client.force_login(user)

    def test
