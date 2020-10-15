from django.db import models


class Policy(models.Model):
    terms_of_use = models.TextField(default='')
    privacy_policy = models.TextField(default='')

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
