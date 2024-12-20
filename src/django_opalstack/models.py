from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Token(models.Model):
    name = models.CharField(
        max_length=50,
    )
    key = models.CharField(
        max_length=200,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user_token",
    )
