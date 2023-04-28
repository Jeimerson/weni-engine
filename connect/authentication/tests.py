from django.test import TestCase
from django.db import IntegrityError

from .models import User


class AuthenticationTestCase(TestCase):
    def test_new_user(self):
        User.objects.create_user("fake@user.com", "fake")

    def test_new_superuser(self):
        User.objects.create_superuser("fake@user.com", "fake")

    def test_new_user_fail_without_email(self):
        with self.assertRaises(ValueError):
            User.objects._create_user("", "fake")

    def test_new_user_fail_without_nickname(self):
        with self.assertRaises(ValueError):
            User.objects._create_user("fake@user.com", "")

    def test_new_superuser_fail_issuperuser_false(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser("fake@user.com", "fake", is_superuser=False)

    def test_user_unique_nickname(self):
        User.objects.create_user("user1@user.com", "fake")
        with self.assertRaises(IntegrityError):
            User.objects.create_user("user2@user.com", "fake")


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="fake",
            email="fake@fake.com",
            first_name="Fake",
            last_name="User",
            language="en"
        )

    def test_update_language(self):
        self.user.update_language("pt_br")
        self.assertEqual(self.user.language, "pt_br")

    def test_token_generator(self):
        self.assertTrue(self.user.token_generator)
