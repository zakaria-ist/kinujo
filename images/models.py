from datetime import date
from django.db import models

def image_container(instance, filename):
    return '/'.join(['prifile', str(instance.id)+'/image', filename])

class Image(models.Model):
    image = models.ImageField(upload_to=image_container)

    is_hidden = models.BooleanField(default=False)
    create_date = models.DateField(default=date.today)
    update_date = models.DateField(default=date.today)
