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
from .insertSerializers import InsertImageSerializer, InsertFinancialAccountSerialier, InsertUserSerializer, InsertGroupSerializer, InsertOrderSerializer, InsertOrderProductSerializer, InsertOrderProductCommissionSerializer, InsertOrderReceiptSerializer, InsertTotalSaleSerializer, InsertTotalCommissionSerializer, InsertPolicySerializer, InsertPrefectureSerializer, InsertProductCategorySerializer, InsertProductSerializer, InsertProductImageSerializer, InsertProductVarietySerializer, InsertProductVarietySelectionSerializer, InsertProductJancodeSerializer, InsertAuthoritySerializer, InsertProfileSerializer, InsertUserSaleSerializer, InsertUserCommisionSerializer, InsertMonthlyPaymentSerializer, InsertAddressSerializer, InsertTaxRateSerializer
from utilities.constants import AUTHORITY_TYPE

def getContext():
    factory = APIRequestFactory()
    n = factory.get('/')
    context = {
        'request': Request(APIRequestFactory().get('/')),
    }
    return context

class CountryCodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CountryCode
        fields = ['name', 'name_jp', 'code', 'tel_code', 'is_hidden', 'created', 'modified']

class ImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'url', 'image', 'is_hidden', 'created', 'modified']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'password', 'groups']

    def create(self, validated_data):
        if "email" not in validated_data:
            validated_data['email'] = validated_data['username'] + "@tmp-kinujo.com"
        user = User.objects.create_user(validated_data['username'], validated_data['email'],
                validated_data['password'])
        return user

class AuthoritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Authority
        fields = ['id', 'url', 'name','commission_rate','official_commission_rate','is_hidden','created','modified']

class ProfileSerializerMinimum(serializers.HyperlinkedModelSerializer):
    authority = AuthoritySerializer()

    class Meta:
        model = Profile
        fields = ['is_master','id','url','authority','is_seller','nickname','is_approved','real_name','is_hidden']
        
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    profit = serializers.SerializerMethodField()
    image = ImageSerializer(required=False)
    background_img = ImageSerializer(required=False)
    authority = AuthoritySerializer()
    bank = serializers.SerializerMethodField()
    email = serializers.CharField(
        allow_blank=True,
        allow_null=True
    )
    # introducer = ProfileSerializer(required=False)

    class Meta:
        model = Profile
        fields = ['is_master', 'tel_code', 'background_img', 'id', 'profit', 'url', 'user','authority','is_seller','shop_name','tel','nickname',
                'user_code','email','introducer','is_approved','image','real_name','gender','birthday','zipcode','prefecture','city','address1',
                'address2','corporate_name','message_notification_phone','message_notification_mail','other_notification_mail','other_notification_phone',
                'allowed_by_id','allowed_by_tel','word','salon_category','is_hidden','created','modified','payload', 'bank', 'representative_name', 'corporate_tel', 'corporate_tel_code']
    def get_profit(self, instance):
        orders = Order.objects.filter(is_hidden=False).values_list('id', flat=True)
        orderProducts = OrderProduct.objects.filter(order__in=orders, is_hidden=False).values_list('id', flat=True)
        if instance.authority_id == AUTHORITY_TYPE['MASTER']:
            # orderProductsCommission = OrderProductCommission.objects.filter(order_product__in=orderProducts, is_hidden=False, user__authority_id=AUTHORITY_TYPE['MASTER'])
            userSale = UserSale.objects.filter(is_hidden=False, user__authority_id=AUTHORITY_TYPE['MASTER'])
            userCommission = UserCommision.objects.filter(is_hidden=False, user__authority_id=AUTHORITY_TYPE['MASTER'])
        else:
            # orderProductsCommission = OrderProductCommission.objects.filter(order_product__in=orderProducts, is_hidden=False, user_id=instance.id)
            userSale = UserSale.objects.filter(is_hidden=False, user_id=instance.id)
            userCommission = UserCommision.objects.filter(is_hidden=False, user_id=instance.id)

        total = 0
        for item in userSale:
            total = total + item.total_amount
        for item in userCommission:
            total = total + item.total_amount
        # for item in orderProducts:
        #     total = total + item.unit_price
        return total
    def get_bank(self, instance):
        bank_account = FinancialAccount.objects.filter(is_hidden=False, user_id=instance.id)
        if bank_account.exists():
            return 1
        else:
            return 0
        

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
class TotalSaleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TotalSale
        fields = ['year','month','sales_amount','tax','amount_tax_included','shipping_fee','total_amount','order_count','is_hidden','created','modified']
class TotalCommissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TotalCommission
        fields = ['year','month','authority','order_count','amount','is_hidden','created','modified']
class PolicySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Policy
        fields = ['privacy_policy', 'terms_of_use','is_hidden','created','modified']
class PrefectureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prefecture
        fields = ['url', 'name', 'name_en', 'is_hidden','created','modified']
class ProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'url', 'name', 'name_en', 'is_hidden','created','modified']
class ProductImageSerializer(serializers.HyperlinkedModelSerializer):
    image = ImageSerializer()
    class Meta:
        model = ProductImage
        fields = ['product','image','is_hidden','created','modified', 'image_no']
class ProductSerializerMinimum(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['name','is_hidden']
class ProductSerializer(serializers.HyperlinkedModelSerializer):
    user = ProfileSerializer()
    category = ProductCategorySerializer()
    productImages = ProductImageSerializer(many=True, required=False)
    productVarieties = InsertProductVarietySerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = ['category', 'productVarieties', 'url', 'id', 'name','brand_name','pr','url_str','category','variety','is_used','is_opened','opened_date','target','price','store_price','shipping_fee','description','is_draft','is_food','is_hidden','created','modified', 'user', 'productImages']
class ProductVarietySerializerMinimum(serializers.HyperlinkedModelSerializer):
    product = ProductSerializerMinimum()
    class Meta:
        model = ProductVariety
        fields = ['product','is_hidden']
class ProductVarietySerializer(serializers.HyperlinkedModelSerializer):
    product = ProductSerializer()
    class Meta:
        model = ProductVariety
        fields = ['url','name','product','vertical_and_horizontal','is_hidden','created','modified']
class ProductVarietySelectionSerializerMinimum(serializers.HyperlinkedModelSerializer):
    product_variety = ProductVarietySerializerMinimum()
    class Meta:
        model = ProductVarietySelection
        fields = ['product_variety','is_hidden']
class ProductVarietySelectionSerializer(serializers.HyperlinkedModelSerializer):
    product_variety = ProductVarietySerializer()
    class Meta:
        model = ProductVarietySelection
        fields = ['product_variety','selection','is_hidden','created','modified']
class ProductJancodeSerializerMinimum(serializers.HyperlinkedModelSerializer):
    horizontal = ProductVarietySelectionSerializerMinimum()
    vertical = ProductVarietySelectionSerializerMinimum()
    class Meta:
        model = ProductJancode
        fields = ['horizontal','vertical','is_hidden']
class ProductJancodeSerializer(serializers.HyperlinkedModelSerializer):
    horizontal = ProductVarietySelectionSerializer()
    vertical = ProductVarietySelectionSerializer()
    class Meta:
        model = ProductJancode
        fields = ['id', 'url', 'horizontal','vertical','jan_code','stock','is_hidden','created','modified']
class OrderReceiptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderReceipt
        fields = ['url', 'id', 'is_copy','to_name','amount','output_date','order_date','product_name','shop_name','order','address','payment','is_hidden','created','modified']
class OrderSerializerMinimum(serializers.HyperlinkedModelSerializer):
    seller = ProfileSerializerMinimum(read_only=True)
   
    class Meta:
        model = Order
        fields = ['id','seller','amount','tax','shipping_fee','total_amount','is_hidden','order_date']
class OrderSerializer(serializers.HyperlinkedModelSerializer):
    seller = ProfileSerializer(read_only=True)
    purchaser = ProfileSerializer(read_only=True)
    prefecture = PrefectureSerializer(read_only=True)
    orderReceipts = OrderReceiptSerializer(many=True, required=False)
    address2 = serializers.CharField(
        allow_blank=True
    )
    shipped_date = serializers.DateField(allow_null=True)
    class Meta:
        model = Order
        fields = ['id', 'orderReceipts', 'seller','purchaser','amount','tax','shipping_fee','total_amount','name','zip1','prefecture','address1','address2','tel','payment',
                'customer_remark','remark','is_hidden','created','modified', 'tel_code', 'shipped_date', 'status', 'card_no']
class OrderProductSerializerMinimum(serializers.HyperlinkedModelSerializer):
    order = OrderSerializerMinimum()
    product_jan_code = ProductJancodeSerializerMinimum()
    class Meta:
        model = OrderProduct
        fields = ['product_jan_code', 'order', 'unit_price','is_hidden']
class OrderProductSerializer(serializers.HyperlinkedModelSerializer):
    order = OrderSerializer()
    product_jan_code = ProductJancodeSerializer()
    class Meta:
        model = OrderProduct
        fields = ['id', 'url', 'product_jan_code', 'order', 'quantity','unit_price','total_price','tax','total_amount','is_hidden','created','modified']
class OrderProductCommissionSerializerMinimum(serializers.HyperlinkedModelSerializer):
    user = ProfileSerializerMinimum(read_only=True)
    order_product = OrderProductSerializerMinimum()
    class Meta:
        model = OrderProductCommission
        fields = ['order_product','user','user_id','amount','is_sales','is_food','is_hidden']
class OrderProductCommissionSerializer(serializers.HyperlinkedModelSerializer):
    user = ProfileSerializer(read_only=True)
    order_product = OrderProductSerializer()
    class Meta:
        model = OrderProductCommission
        fields = ['id', 'order_product','user','user_id','amount','is_sales','is_food','shipping_fee','is_hidden','created','modified']

class FinancialAccountSerialier(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FinancialAccount
        fields = ['url', 'user','financial_name','financial_code','account_type','branch_code','branch_name','account_number','account_name','is_hidden','created','modified']

class UserSaleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserSale
        fields = ['year','month','user','order_count','sales_amount','tax','amount_tax_included','shipping_fee','total_amount','is_hidden','created','modified']

class UserCommisionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserCommision
        fields = ['year','month','user','order_count','amount','tax','total_amount','is_hidden','created','modified']
class MonthlyPaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MonthlyPayment
        fields = ['year','month','user','amount','paid_date','status','is_hidden','created','modified']
class AddressSerializer(serializers.HyperlinkedModelSerializer):
    address2 = serializers.CharField(
        allow_blank=True
    )
    tel_code = serializers.CharField(allow_null=False, allow_blank=False)
    prefecture = PrefectureSerializer()
    class Meta:
        model = Address
        fields = ['id', 'url', 'address_name','user','name','zip1','prefecture','address1','address2','tel','is_default','is_hidden','created','modified', 'tel_code']
class TaxRateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaxRate
        fields = ['url', 'id', 'start_date','end_date','tax_rate','reduced_tax_rate','is_hidden','created','modified']
