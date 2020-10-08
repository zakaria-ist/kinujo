from datetime import date, datetime
from django.db import models
from products.models import ProductJancode
from profiles.models import Profile, Authority
from prefectures.models import Prefecture
from django.core.validators import MaxValueValidator


class Order(models.Model):
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='order_seller')
    purchaser = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='order_purchaser')
    amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    tax = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    shipping_fee = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    total_amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    name = models.CharField(max_length=128)
    zip1 = models.CharField(max_length=8)
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=1024)
    address2 = models.CharField(max_length=1024, default='')
    tel = models.CharField(max_length=32)
    payment = models.CharField(max_length=255)
    customer_remark = models.TextField(default='')
    remark = models.TextField(default='')

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class OrderProduct(models.Model):
    product_jan_code = models.ForeignKey(ProductJancode, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    unit_price = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    total_price = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    tax = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    total_amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class OrderProductCommission(models.Model):
    order_product = models.ForeignKey(OrderProduct, on_delete=models.CASCADE)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    is_sales = models.BooleanField(default=False)
    is_food = models.BooleanField(default=False)
    shipping_fee = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class OrderReceipt(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    is_copy = models.BooleanField(default=False)
    to_name = models.CharField(max_length=255)
    amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    output_date = models.DateField(default=date.today)
    order_date = models.DateField(default=datetime.now)
    product_name = models.CharField(max_length=255)
    shop_name = models.CharField(max_length=255)
    address = models.TextField()
    payment = models.TextField()

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class TotalSale(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    sales_amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    tax = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    amount_tax_included = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    shipping_fee = models.IntegerField(validators=[MaxValueValidator(99999999999)], default=0)
    total_amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    order_count = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class TotalCommission(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    order_count = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
