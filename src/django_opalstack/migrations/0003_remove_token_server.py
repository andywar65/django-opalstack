# Generated by Django 5.1.4 on 2024-12-20 08:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("django_opalstack", "0002_rename_value_token_key_alter_token_server"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="token",
            name="server",
        ),
    ]
