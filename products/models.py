from datetime import date
from django.db import models
from images.models import Image
from profiles.models import Profile
from django.core.validators import MaxValueValidator
from utilities.constants import PRODUCT_VARIETY, TARGET_TYPE

class ProductCategory(models.Model):
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255, default='')

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)

class Product(models.Model):
    name = models.CharField(max_length=128, blank=True, null=True)
    brand_name = models.CharField(max_length=128, blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_product', null=False)
    pr = models.TextField(blank=True, null=True)
    url_str = models.CharField(max_length=255, blank=True, null=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, null=True, blank=True)
    variety = models.SmallIntegerField(null=True, choices=PRODUCT_VARIETY, blank=True)
    is_used = models.BooleanField(default=False, null=True)
    is_opened = models.BooleanField(default=False, null=True)
    opened_date = models.DateField(null=True, default=date.today, blank=True)
    target = models.SmallIntegerField(null=True, choices=TARGET_TYPE, blank=True)
    price = models.BigIntegerField(validators=[MaxValueValidator(99999999999)], default=0, null=True, blank=True)
    store_price = models.DecimalField(max_digits=11, decimal_places=2, default=0, null=True, blank=True)
    shipping_fee = models.DecimalField(max_digits=11, decimal_places=2, default=0, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    is_draft = models.BooleanField(default=False, null=True)
    is_food = models.BooleanField(default=False, null=True)

    is_hidden = models.BooleanField(default=False, null=True)
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
    name = models.CharField(max_length=100, default='', blank=True, null=True)
    product = models.ForeignKey(Product, related_name='productVarieties', on_delete=models.CASCADE)
    vertical_and_horizontal = models.SmallIntegerField(null=True, choices=PRODUCT_VARIETY)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class ProductVarietySelection(models.Model):
    product_variety = models.ForeignKey(ProductVariety, related_name='productVarietySelections', on_delete=models.CASCADE, null=True)
    selection = models.CharField(max_length=255, default='', blank=True, null=True)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class ProductJancode(models.Model):
    horizontal = models.ForeignKey(ProductVarietySelection, on_delete=models.CASCADE, related_name='jancode_horizontal', null=True)
    vertical = models.ForeignKey(ProductVarietySelection, on_delete=models.CASCADE, related_name='jancode_vertical', null=True)
    jan_code = models.CharField(max_length=255, default='', blank=True, null=True)
    stock = models.BigIntegerField(validators=[MaxValueValidator(99999999999)], default=0)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
