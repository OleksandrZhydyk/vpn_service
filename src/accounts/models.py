from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    user = models.OneToOneField(
        to=get_user_model(), on_delete=models.CASCADE, primary_key=True, related_name="profile"
    )
    created_at = models.DateTimeField(auto_now=True, null=True, editable=False, verbose_name="Modified date")
    photo = models.ImageField(
        default="/empty_avatar.png",
        null=True,
        blank=True,
        upload_to="profiles_avatars/%Y/%m/%d/",
        verbose_name="Avatar",
    )
    first_name = models.CharField(_("First name"), max_length=150, blank=True)
    last_name = models.CharField(_("Last name"), max_length=150, blank=True)

    def __str__(self):
        return str(self.user)
