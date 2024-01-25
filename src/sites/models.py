from django.contrib.auth import get_user_model
from django.db import models


class Site(models.Model):
    url = models.URLField()
    name = models.CharField(max_length=50)
    moves_by_pages = models.PositiveIntegerField(default=0)
    upload_data_size = models.FloatField(default=0)
    received_data_size = models.FloatField(default=0)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="statistics")
