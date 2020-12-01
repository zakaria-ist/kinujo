from django.contrib.auth.models import User, Group
from orders.models import Order, OrderProduct, OrderProductCommission, OrderReceipt, TotalSale, TotalCommission
from policies.models import Policy
from prefectures.models import Prefecture
from products.models import ProductCategory, Product, ProductImage, ProductVariety, ProductVarietySelection, ProductJancode
from profiles.models import FinancialAccount, Authority, Profile, UserSale, UserCommision, MonthlyPayment, Address
from taxes.models import TaxRate
from images.models import Image
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.test import APIRequestFactory
from rest_framework.request import Request

def getContext():
    factory = APIRequestFactory()
    n = factory.get('/')
    context = {
        'request': Request(APIRequestFactory().get('/')),
    }
    return context

class InsertImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Image
        fields = ['url', 'image', 'is_hidden', 'created', 'modified']
        
class InsertUserSerializer(serializers.HyperlinkedModelSerializer):
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
    
class InsertAuthoritySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Authority
        fields = ['id', 'url', 'name','commission_rate','official_commission_rate','is_hidden','created','modified']

class InsertProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ['background_img', 'id', 'url', 'user','authority','is_seller','shop_name','tel','password','nickname','user_code','email','introducer','is_approved','image','real_name','gender','birthday','zipcode','prefecture','city','address1','address2','corporate_name','message_notification_phone','message_notification_mail','other_notification_mail','other_notification_phone','allowed_by_id','allowed_by_tel','word','salon_category','is_hidden','created','modified','payload']

class InsertGroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
class InsertTotalSaleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TotalSale
        fields = ['year','month','sales_amount','tax','amount_tax_included','shipping_fee','total_amount','order_count','is_hidden','created','modified']
class InsertTotalCommissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TotalCommission
        fields = ['year','month','authority','order_count','amount','is_hidden','created','modified']
class InsertPolicySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Policy
        fields = ['privacy_policy','is_hidden','created','modified']
class InsertPrefectureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Prefecture
        fields = ['url', 'name','is_hidden','created','modified']
class InsertProductCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['name','is_hidden','created','modified']
class InsertProductImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['product','image','is_hidden','created','modified',]
class InsertProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['url', 'id', 'name','brand_name','pr','url_str','category','variety','is_used','is_opened','opened_date','target','price','store_price','shipping_fee','description','is_draft','is_food','is_hidden','created','modified', 'user']
class InsertProductJancodeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProductJancode
        fields = ['url', 'id', 'horizontal','vertical','jan_code','stock','is_hidden','created','modified']
class InsertProductVarietySelectionSerializer(serializers.HyperlinkedModelSerializer):
    jancode_horizontal = InsertProductJancodeSerializer(many=True, required=False)
    jancode_vertical = InsertProductJancodeSerializer(many=True, required=False)
    class Meta:
        model = ProductVarietySelection
        fields = ['url', 'id', 'jancode_horizontal', 'jancode_vertical', 'product_variety','selection','is_hidden','created','modified']
class InsertProductVarietySerializer(serializers.HyperlinkedModelSerializer):
    productVarietySelections = InsertProductVarietySelectionSerializer(many=True, required=False)
    class Meta:
        model = ProductVariety
        fields = ['url', 'id', 'productVarietySelections', 'name','product','vertical_and_horizontal','is_hidden','created','modified']
class InsertOrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'url', 'seller','purchaser','amount','tax','shipping_fee','total_amount','name','zip1','prefecture','address1','address2','tel','payment','customer_remark','remark','is_hidden','created','modified', 'status']
class InsertOrderProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['id', 'url', 'product_jan_code', 'order', 'quantity','unit_price','total_price','tax','total_amount','is_hidden','created','modified']
class InsertOrderProductCommissionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderProductCommission
        fields = ['order_product','user','amount','is_sales','is_food','shipping_fee','is_hidden','created','modified']
class InsertOrderReceiptSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderReceipt
        fields = ['is_copy','to_name','amount','output_date','order_date','product_name','shop_name','address','payment','is_hidden','created','modified']
        
class InsertFinancialAccountSerialier(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = FinancialAccount
        fields = ['url', 'user','financial_name','financial_code','account_type','branch_code','branch_name','account_number','account_name','is_hidden','created','modified']

class InsertUserSaleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserSale
        fields = ['year','month','user','order_count','sales_amount','tax','amount_tax_included','shipping_fee','total_amount','is_hidden','created','modified']

class InsertUserCommisionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserCommision
        fields = ['year','month','user','order_count','amount','tax','total_amount','is_hidden','created','modified']
class InsertMonthlyPaymentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MonthlyPayment
        fields = ['year','month','user','amount','paid_date','status','is_hidden','created','modified']
class InsertAddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'url', 'address_name','user','name','zip1','prefecture','address1','address2','tel','is_default','is_hidden','created','modified']
class InsertTaxRateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TaxRate
        fields = ['start_date','end_date','tax_rate','reduced_tax_rate','is_hidden','created','modified']


