from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from api.models import CustomUser


class CustomUserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.username = 'testuser1'
        cls.password = 'Ltye$4T5'
        cls.email = 'user1@test.com'
        cls.invalid_email = 'user1'

    def test_custom_user_creation_with_necessary_fields(self):
        custom_user = CustomUser.objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
        )
        self.assertTrue(isinstance(custom_user, CustomUser))
        self.assertEqual(custom_user.username, self.username)
        self.assertEqual(custom_user.email, self.email)
        self.assertTrue(custom_user.check_password(self.password))
        self.assertFalse(custom_user.is_authority)

    def test_custom_user_creation_with_empty_username(self):
        with self.assertRaisesMessage(ValueError, 'The username must be set'):
            custom_user = CustomUser.objects.create_user(
                username='',
                email=self.email,
                password=self.password,
            )

    def test_custom_user_creation_with_empty_email(self):
        with self.assertRaisesMessage(ValueError, 'The email must be set'):
            custom_user = CustomUser.objects.create_user(
                username=self.username,
                email='',
                password=self.password,
            )

    def test_custom_user_creation_with_invalid_email(self):
        with self.assertRaises(ValidationError):
            custom_user = CustomUser.objects.create_user(
                username=self.username,
                email=self.invalid_email,
                password=self.password,
            )

    def test_custom_user_creation_with_duplicate_email(self):
        with self.assertRaises(IntegrityError):
            custom_user_1 = CustomUser.objects.create_user(
                username=self.username,
                email=self.email,
                password=self.password,
            )
            custom_user_2 = CustomUser.objects.create_user(
                username='different_user',
                email=self.email,
                password=self.password,
            )

    def test_custom_user_creation_with_empty_password(self):
        with self.assertRaisesMessage(ValueError, 'The password must be set'):
            custom_user = CustomUser.objects.create_user(
                username=self.username,
                email=self.email,
                password='',
            )
