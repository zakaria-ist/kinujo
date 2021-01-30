from django.contrib.auth.models import User, Group
from orders.models import Order, OrderProduct, OrderProductCommission, OrderReceipt, TotalSale, TotalCommission
from policies.models import Policy
from prefectures.models import Prefecture, CountryCode
from products.models import ProductCategory, Product, ProductImage, ProductVariety, ProductVarietySelection, ProductJancode
from profiles.models import FinancialAccount, Authority, Profile, UserSale, UserCommision, MonthlyPayment, Address
from taxes.models import TaxRate
from images.models import Image
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request
from django.db import models

def getContext():
    factory = APIRequestFactory()
    n = factory.get('/')
    context = {
        'request': Request(APIRequestFactory().get('/')),
    }
    return context

class AuthoritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Authority
        fields = ['id']

class SimpleProduct_ProfileSerializer(serializers.HyperlinkedModelSerializer):
    authority = AuthoritySerializer()
    class Meta:
        model = Profile
        fields = ['authority', 'shop_name']

class SimpleProduct_ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'url', 'image', 'is_hidden']

class SimpleProduct_ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    image = SimpleProduct_ImageSerializer()
    class Meta:
        model = ProductImage
        fields = ['product','image','is_hidden']

class SimpleProduct_ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'url', 'name']

class SimpleProductSerializer(serializers.HyperlinkedModelSerializer):
    user = SimpleProduct_ProfileSerializer()
    category = SimpleProduct_ProductCategorySerializer()
    productImages = SimpleProduct_ProductImageSerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = ['url', 'id', 'name','brand_name','category','is_used','is_opened','opened_date','price','store_price','shipping_fee','is_draft','is_food','is_hidden','created','modified','user','productImages']
