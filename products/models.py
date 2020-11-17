from datetime import date
from django.db import models
from images.models import Image
from profiles.models import Profile
from django.core.validators import MaxValueValidator
from utilities.constants import PRODUCT_VARIETY, TARGET_TYPE

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=128)
    brand_name = models.CharField(max_length=128, default='')
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_product', null=False)
    pr = models.TextField()
    url_str = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    variety = models.SmallIntegerField(null=True, choices=PRODUCT_VARIETY)
    is_used = models.BooleanField(default=False)
    is_opened = models.BooleanField(default=False)
    opened_date = models.DateField(default=date.today)
    target = models.SmallIntegerField(null=True, choices=TARGET_TYPE)
    price = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    store_price = models.DecimalField(max_digits=11, decimal_places=2)
    shipping_fee = models.DecimalField(max_digits=11, decimal_places=2)
    description = models.TextField()
    is_draft = models.BooleanField(default=False)
    is_food = models.BooleanField(default=False)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='productImages', on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    image_no = models.SmallIntegerField(null=True)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class ProductVariety(models.Model):
    name = models.CharField(max_length=100, default='')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    vertical_and_horizontal = models.SmallIntegerField(null=True, choices=PRODUCT_VARIETY)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class ProductVarietySelection(models.Model):
    product_variety = models.ForeignKey(ProductVariety, on_delete=models.CASCADE, null=True)
    selection = models.CharField(max_length=255, default='')

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class ProductJancode(models.Model):
    horizontal = models.ForeignKey(ProductVarietySelection, on_delete=models.CASCADE, related_name='jancode_horizontal', null=True)
    vertical = models.ForeignKey(ProductVarietySelection, on_delete=models.CASCADE, related_name='jancode_vertical', null=True)
    jan_code = models.CharField(max_length=255, default='')
    stock = models.BigIntegerField(validators=[MaxValueValidator(99999999999)], default=0)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
