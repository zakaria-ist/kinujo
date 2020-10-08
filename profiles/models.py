from django.db import models
from images.models import Image
from prefectures.models import Prefecture
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator
from utilities.constants import GENDER_TYPE, SALON_TYPE, PAYMENT_STATUS


class Authority(models.Model):
    name = models.CharField(max_length=128)
    commission_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    official_commission_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0)
    is_enable = models.BooleanField(default=True)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    authority = models.ForeignKey(Authority, on_delete=models.CASCADE)
    is_seller = models.BooleanField(default=False)
    shop_name = models.CharField(max_length=255, default='')
    tel = models.CharField(max_length=15)
    password = models.CharField(max_length=20)
    nickname = models.CharField(max_length=255)
    user_code = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, default='')
    introducer = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    is_approved = models.BooleanField(default=False)
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True)
    real_name = models.CharField(max_length=255, default='')
    gender = models.SmallIntegerField(null=True, choices=tuple([status[::-1] for status in GENDER_TYPE]))
    birthday = models.DateField(null=True)
    zipcode = models.CharField(max_length=7, default='')
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE, null=True)
    city = models.CharField(max_length=100, default='')
    address1 = models.CharField(max_length=255, default='')
    address2 = models.CharField(max_length=255, default='')
    corporate_name = models.CharField(max_length=255, default='')
    message_notification = models.BooleanField(default=False)
    other_notification = models.BooleanField(default=False)
    allowed_by_id = models.BooleanField(default=False)
    allowed_by_tel = models.BooleanField(default=False)
    word = models.CharField(max_length=255, default='')
    salon_category = models.SmallIntegerField(null=True, choices=tuple([status[::-1] for status in SALON_TYPE]))

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class UserSale(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    order_count = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    sales_amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    tax = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    amount_tax_included = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    shipping_fee = models.BigIntegerField(validators=[MaxValueValidator(99999999999)], default=0)
    total_amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class UserCommision(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    order_count = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    tax = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    total_amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class MonthlyPayment(models.Model):
    year = models.IntegerField()
    month = models.IntegerField()
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    amount = models.BigIntegerField(validators=[MaxValueValidator(99999999999)])
    paid_date = models.DateField(null=True)
    status = models.SmallIntegerField(null=True, choices=tuple([status[::-1] for status in PAYMENT_STATUS]))

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)


class Address(models.Model):
    address_name = models.CharField(max_length=128)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    zip1 = models.CharField(max_length=8)
    prefecture = models.ForeignKey(Prefecture, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=1024)
    address2 = models.CharField(max_length=1024, default='')
    tel = models.CharField(max_length=32)
    is_default = models.BooleanField(default=False)

    is_hidden = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
