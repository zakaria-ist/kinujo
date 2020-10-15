from django.db import models

def image_container(instance, filename):
    return '/'.join(['profile', '/image', filename])

class Image(models.Model):
    image = models.ImageField(upload_to=image_container)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
