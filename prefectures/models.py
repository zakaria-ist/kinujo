from django.db import models


class Prefecture(models.Model):
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, default='')
    is_enable = models.BooleanField(default=True)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

class CountryCode(models.Model):
    name = models.CharField(max_length=100)
    name_jp = models.CharField(max_length=100, default='')
    code = models.CharField(max_length=10, default='')
    tel_code = models.CharField(max_length=10, default='')

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
