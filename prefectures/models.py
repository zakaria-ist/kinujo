from django.db import models


class Prefecture(models.Model):
    name = models.CharField(max_length=255)
    is_enable = models.BooleanField(default=True)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

class CountryCode(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, default='')
    tel_code = models.CharField(max_length=10, default='')

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
