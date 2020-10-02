from datetime import date
from django.db import models


class Policy(models.Model):
    terms_of_use = models.TextField(default='')
    privacy_policy = models.TextField(default='')
    
    is_hidden = models.BooleanField(default=False)
    create_date = models.DateField(default=date.today)
    update_date = models.DateField(default=date.today)
