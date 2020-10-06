from datetime import date
from django.db import models
from prefectures.models import Prefecture
from profiles.models import Profile


class Salons(models.Model):
    name = models.CharField(max_length=128)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    zip1 = models.CharField(max_length=8)
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=1024)
    address2 = models.CharField(max_length=1024, default='')
    tel = models.CharField(max_length=32)
    pic_name = models.CharField(max_length=128)
    pic_tel = models.CharField(max_length=32)

    is_hidden = models.BooleanField(default=False)
    create_date = models.DateField(default=date.today)
    update_date = models.DateField(default=date.today)
