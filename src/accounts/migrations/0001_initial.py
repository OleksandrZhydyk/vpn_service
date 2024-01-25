# Generated by Django 5.0.1 on 2024-01-23 18:42

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="profile",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now=True, null=True, verbose_name="Modified date"
                    ),
                ),
                (
                    "photo",
                    models.ImageField(
                        blank=True,
                        default="/empty_avatar.png",
                        null=True,
                        upload_to="profiles_avatars/%Y/%m/%d/",
                        verbose_name="Avatar",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="First name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="Last name"
                    ),
                ),
            ],
        ),
    ]
