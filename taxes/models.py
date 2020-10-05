from datetime import date
from django.db import models


class TaxRate(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    reduced_tax_rate = models.DecimalField(max_digits=5, decimal_places=2)

    is_hidden = models.BooleanField(default=False)
    create_date = models.DateField(default=date.today)
    update_date = models.DateField(default=date.today)
