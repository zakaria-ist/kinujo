from datetime import date
from django.db import models


class Image(models.Model):
    image_path = models.CharField(max_length=255)

    is_hidden = models.BooleanField(default=False)
    create_date = models.DateField(default=date.today)
    update_date = models.DateField(default=date.today)
