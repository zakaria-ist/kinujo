from datetime import date
from django.db import models


class Prefecture(models.Model):
    name = models.CharField(max_length=100)
    
    is_hidden = models.BooleanField(default=False)
    create_date = models.DateField(default=date.today)
    update_date = models.DateField(default=date.today)
