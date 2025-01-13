from django.contrib.auth.models import User
from django.test import TestCase, override_settings
from django.urls import reverse
from environs import Env

from django_opalstack.models import Token

env = Env()
env.read_env()
OPAL_KEY = env.str("OPAL_KEY")


@override_settings(DEBUG=False)
class OpalstackViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_superuser("boss", "test@example.com", "p4s5w0r6")
        User.objects.create_superuser("impostor", "impostor@example.com", "p4s5w0r6")
        Token.objects.create(
            name="test_token",
            key=OPAL_KEY,
            user=user,
        )

    def test_unlogged_status_code(self):
        response = self.client.get(
            reverse(
                "django_opalstack:token_list",
            )
        )
        self.assertEqual(response.status_code, 302)
        token = Token.objects.get(name="test_token")
        response = self.client.get(
            reverse(
                "django_opalstack:token_detail",
                kwargs={"pk": token.id},
            )
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            reverse(
                "django_opalstack:user_list",
                kwargs={"pk": token.id},
            )
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            reverse(
                "django_opalstack:app_list",
                kwargs={"pk": token.id},
            )
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            reverse(
                "django_opalstack:site_list",
                kwargs={"pk": token.id},
            )
        )
        self.assertEqual(response.status_code, 302)
        response = self.client.get(
            reverse(
                "django_opalstack:app_detail",
                kwargs={"pk": token.id},
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_impostor_login_status_code(self):
        self.client.login(username="impostor", password="p4s5w0r6")
        response = self.client.get(
            reverse(
                "django_opalstack:token_list",
            )
        )
        self.assertEqual(response.status_code, 200)
        token = Token.objects.get(name="test_token")
        response = self.client.get(
            reverse(
                "django_opalstack:token_detail",
                kwargs={"pk": token.id},
            )
        )
        self.assertEqual(response.status_code, 403)
        response = self.client.get(
            reverse(
                "django_opalstack:user_list",
                kwargs={"pk": token.id},
            )
        )
        self.assertEqual(response.status_code, 403)
        response = self.client.get(
            reverse(
                "django_opalstack:app_list",
                kwargs={"pk": token.id},
            )
        )
        self.assertEqual(response.status_code, 403)
        response = self.client.get(
            reverse(
                "django_opalstack:site_list",
                kwargs={"pk": token.id},
            )
        )
        self.assertEqual(response.status_code, 403)
        response = self.client.get(
            reverse(
                "django_opalstack:app_detail",
                kwargs={"pk": token.id},
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_boss_login_status_code(self):
        self.client.login(username="boss", password="p4s5w0r6")
        token = Token.objects.get(name="test_token")
        response = self.client.get(
            reverse(
                "django_opalstack:token_detail",
                kwargs={"pk": token.id},
            )
        )
        self.assertEqual(response.status_code, 200)
