from datetime import date
from django.db import models


class TaxRate(models.Model):
    start_date = models.DateField(default=date.today)
    end_date = models.DateField(null=True)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    reduced_tax_rate = models.DecimalField(max_digits=5, decimal_places=2)
    is_enable = models.BooleanField(default=True)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
