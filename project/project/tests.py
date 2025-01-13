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
