import requests
import json
import stripe
import ast
import uuid
import string
import random
from django.conf import settings
from datetime import date
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import activate, deactivate_all
from .serializers import CountryCodeSerializer, ImageSerializer, FinancialAccountSerialier, UserSerializer, GroupSerializer,  OrderSerializer, OrderProductSerializer, OrderProductCommissionSerializer, OrderReceiptSerializer, TotalSaleSerializer, TotalCommissionSerializer, PolicySerializer, PrefectureSerializer, ProductCategorySerializer, ProductSerializer, ProductImageSerializer, ProductVarietySerializer, ProductVarietySelectionSerializer, ProductJancodeSerializer, AuthoritySerializer, ProfileSerializer, UserSaleSerializer, UserCommisionSerializer, MonthlyPaymentSerializer, AddressSerializer, TaxRateSerializer
from .insertSerializers import InsertImageSerializer, InsertFinancialAccountSerialier, InsertUserSerializer, InsertGroupSerializer, InsertOrderSerializer, InsertOrderProductSerializer, InsertOrderProductCommissionSerializer, InsertOrderReceiptSerializer, InsertTotalSaleSerializer, InsertTotalCommissionSerializer, InsertPolicySerializer, InsertPrefectureSerializer, InsertProductCategorySerializer, InsertProductSerializer, InsertProductImageSerializer, InsertProductVarietySerializer, InsertProductVarietySelectionSerializer, InsertProductJancodeSerializer, InsertAuthoritySerializer, InsertProfileSerializer, InsertUserSaleSerializer, InsertUserCommisionSerializer, InsertMonthlyPaymentSerializer, InsertAddressSerializer, InsertTaxRateSerializer
from .simpleProductSerializers import SimpleProductSerializer
from rest_framework.test import APIRequestFactory
from rest_framework.parsers import MultiPartParser
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from orders.models import Order, OrderProduct, OrderProductCommission, OrderReceipt, TotalSale, TotalCommission
from policies.models import Policy
from images.models import Image
from rest_framework import filters
from prefectures.models import Prefecture, CountryCode
from products.models import ProductCategory, Product, ProductImage, ProductVariety, ProductVarietySelection, ProductJancode
from profiles.models import FinancialAccount, Authority, Profile, UserSale, UserCommision, MonthlyPayment, Address
from taxes.models import TaxRate
from orders.views import if_kinujo_product
from utilities.constants import AUTHORITY_TYPE

def getContext():
    factory = APIRequestFactory()
    n = factory.get('/')
    context = {
        'request': Request(APIRequestFactory().get('/')),
    }
    return context

def getObject(url):
    url = url.replace("testserver", "192.168.0.107:8000")
    return requests.get(url = url).json()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class ImageViewSet(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CountryCodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = CountryCode.objects.all()
    serializer_class = CountryCodeSerializer

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

class OrderProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = OrderProduct.objects.all()
    serializer_class = OrderProductSerializer

class OrderProductCommissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = OrderProductCommission.objects.all()
    serializer_class = OrderProductCommissionSerializer

class OrderReceiptViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = OrderReceipt.objects.all()
    serializer_class = OrderReceiptSerializer

class TotalSaleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TotalSale.objects.all()
    serializer_class = TotalSaleSerializer

class TotalCommissionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TotalCommission.objects.all()
    serializer_class = TotalCommissionSerializer

class PolicyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Policy.objects.filter(is_hidden=0)
    serializer_class = PolicySerializer

class PrefectureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Prefecture.objects.all()
    serializer_class = PrefectureSerializer

class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class SimpleProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = SimpleProductSerializer

class ProductImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer

class ProductVarietyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ProductVariety.objects.all()
    serializer_class = ProductVarietySerializer

class ProductVarietySelectionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ProductVarietySelection.objects.all()
    serializer_class = ProductVarietySelectionSerializer

class ProductJancodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = ProductJancode.objects.all()
    serializer_class = ProductJancodeSerializer

class AuthorityViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Authority.objects.all()
    serializer_class = AuthoritySerializer

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Profile.objects.all()
    search_fields = ['nickname', 'user_code']
    filter_backends = [filters.SearchFilter]
    serializer_class = ProfileSerializer

class FinancialAccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = FinancialAccount.objects.all()
    serializer_class = FinancialAccountSerialier

class UserSaleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = UserSale.objects.all()
    serializer_class = UserSaleSerializer

class UserCommisionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = UserCommision.objects.all()
    serializer_class = UserCommisionSerializer

class MonthlyPaymentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = MonthlyPayment.objects.all()
    serializer_class = MonthlyPaymentSerializer

class AddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class InsertAddressViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Address.objects.all()
    serializer_class = InsertAddressSerializer

class TaxRateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TaxRate.objects.all()
    serializer_class = TaxRateSerializer

class UserImages(APIView):
    def post(self, request, format='json'):
        profiles = Profile.objects.filter(id__in=request.data['users'], is_hidden=False)
        profileSerializer = ProfileSerializer(profiles, many=True, context=getContext())
        images = []
        for profile in profileSerializer.data:
            if profile['image'] and profile['image']['image']:
                images.append(profile['image']['image'])
            else:
                images.append("")
        return Response({"success" : False, "images": images}, status=status.HTTP_200_OK)

class AllUserImages(APIView):
    def post(self, request, format='json'):
        profiles = Profile.objects.filter(is_hidden=False)
        profileSerializer = ProfileSerializer(profiles, many=True, context=getContext())
        users = []
        for profile in profileSerializer.data:
            users.append({
                'id': str(profile['id']),
                'name': str(profile['nickname']),
                'image': profile['image']['image'] if profile['image'] and profile['image']['image'] else ""
            })
        return Response({"success" : False, "users": users}, status=status.HTTP_200_OK)

class UserRegister(APIView):
    def post(self, request, format='json'):
        try:
            userItem = request.data
            userItem['username'] = str("+") + str(userItem['username'])
            userItem['email'] = str("+") + str(userItem['username']) + str("-") + str(uuid.uuid4()) + "@tmp-kinujo.com"

            userSerializer = UserSerializer(data=userItem, context=getContext())
            if userSerializer.is_valid():
                user = userSerializer.save()

                authority = Authority.objects.get(id=5)
                is_seller = 0
                if request.data['authority'] == 'store':
                    authority = Authority.objects.get(id=4)
                    is_seller = 1

                authoritySerializer = AuthoritySerializer(authority, context=getContext())
                yetToComplete = True
                user_code = ""
                while yetToComplete:
                    user_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
                    existing_profile = Profile.objects.filter(is_hidden=False, user_code=user_code)
                    if not existing_profile.count():
                        yetToComplete = False
                profileItem = {
                    'user' : userSerializer.data['url'],
                    'tel' : request.data['username'].replace("+" + request.data['callingCode'], ""),
                    'nickname' : request.data['nickname'],
                    'user_code' : user_code,
                    'authority' : authoritySerializer.data['url'],
                    'is_seller' : is_seller,
                    'tel_code': "+" + request.data['callingCode']
                }
                if request.data['introducer']:
                    introducerProfile = None
                    try:
                        introducerProfile = Profile.objects.get(id=int(request.data['introducer']), is_hidden=False)
                    except Exception as e:
                        print(e)
                    if introducerProfile:
                        introducerProfileSerializer = InsertProfileSerializer(introducerProfile, context=getContext())
                        profileItem['introducer'] = introducerProfileSerializer.data['url']
                else:
                    introducerProfile = None
                    try:
                        introducerProfile = Profile.objects.get(is_master=1, is_hidden=False)
                    except Exception as e:
                        print(e)
                    if introducerProfile:
                        introducerProfileSerializer = InsertProfileSerializer(introducerProfile, context=getContext())
                        profileItem['introducer'] = introducerProfileSerializer.data['url']

                profileItem["email"] = ""
                profileSerializer = InsertProfileSerializer(data=profileItem, context=getContext())
                if profileSerializer.is_valid():
                    profile = profileSerializer.save()
                    if user:
                        data = profileSerializer.data
                        # data['authority'] = getObject(data['authority'])
                        # data['user'] = getObject(data['user'])
                        return Response({"success": True, "data" : {
                            "user" : data
                        }}, status=status.HTTP_201_CREATED)
                else:
                    print(profileSerializer.errors)
                    return Response({"success" : False, "errors" : profileSerializer.errors}, status=status.HTTP_200_OK)
            else:
                print(userSerializer.errors)
                return Response({"success" : False, "errors": userSerializer.errors}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success" : False, "error": str(e)}, status=status.HTTP_200_OK)

class CheckRegister(APIView):
    def post(self, request, format='json'):
        userSerializer = UserSerializer(data=request.data, context=getContext())
        if userSerializer.is_valid():
            data2 = request.data
            data2['username'] = "+" + data2['username']
            userSerializer2 = UserSerializer(data=data2, context=getContext())
            if userSerializer2.is_valid():
                return Response({"success" : True}, status=status.HTTP_200_OK)
            return Response({"success" : False, "errors" : userSerializer2.errors}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "errors" : userSerializer.errors}, status=status.HTTP_200_OK)

class UserLogin(APIView):
    def post(self, request, format='json'):
        user = None
        try:
            user = User.objects.get(username = request.data['tel'])
        except Exception as e:
            print(e)

        if user is None:
            try:
                user = User.objects.get(username = "+" + request.data['tel'])
            except Exception as e:
                print(e)

        if user:
            profile = None
            try:
                profile = Profile.objects.get(user_id=user.id, is_hidden=False)
            except Exception as e:
                print(e)

            if profile:
                if user.check_password(request.data['password']):
                    profileSerializer = ProfileSerializer(profile, context=getContext())
                    data = profileSerializer.data
                    # data['authority'] = getObject(data['authority'])
                    # data['user'] = getObject(data['user'])
                    return Response({"success" : True, "data" : {
                        "user" : data
                    }}, status=status.HTTP_200_OK)
                else:
                    return Response({"success" : False, "error" : "入力された情報が正しくありません"}, status=status.HTTP_200_OK)
                    return Response({"success" : False, "error" : "Incorrect Password"}, status=status.HTTP_200_OK)
            else:
                return Response({"success" : False, "error" : "入力された情報が正しくありません"}, status=status.HTTP_200_OK)
                return Response({"success" : False, "error" : "Account Not Exists"}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "error" : "入力された情報が正しくありません"}, status=status.HTTP_200_OK)
            return Response({"success" : False, "error" : "Account Not Exists"}, status=status.HTTP_200_OK)

class PasswordReset(APIView):
    def post(self, request, format='json'):
        profile = None
        try:
            profile = Profile.objects.get(tel=request.data['tel_code'] + request.data['tel'], is_hidden=False)
        except Exception as e:
            print(e)

        if profile is None:
            try:
                profile = Profile.objects.get(tel = "+" + request.data['tel_code'] + request.data['tel'], is_hidden=False)
            except Exception as e:
                print(e)

        if profile is None:
            try:
                profile = Profile.objects.get(tel = request.data['tel'], is_hidden=False)
            except Exception as e:
                print(e)

        if profile:
            user = None
            try:
                user = User.objects.get(id = profile.user_id)
            except Exception as e:
                print(e)
            if user:
                if request.data['password'] == request.data['confirm_password']:
                    user.set_password(request.data['password'])
                    user.save()

                    return Response({"success" : True}, status=status.HTTP_200_OK)
                else:
                    return Response({"success" : False, "error" : "password_mismatch"}, status=status.HTTP_200_OK)
            else:
                return Response({"success" : False, "error" : "account_not_exists"}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "error" : "account_not_exists"}, status=status.HTTP_200_OK)

class ChangeEmail(APIView):
    def post(self, request, format='json'):
        profile = None
        try:
            profile = Profile.objects.get(tel=request.data['tel'], is_hidden=False)
        except Exception as e:
            print(e)

        if profile is None:
            try:
                profile = Profile.objects.get(tel = "+" + request.data['tel'], is_hidden=False)
            except Exception as e:
                print(e)

        if profile:
            user = None
            try:
                user = User.objects.get(id = profile.user_id)
            except Exception as e:
                print(e)
            if user:
                    user.email = request.data['email']
                    user.save()

                    profile.email = request.data['email']
                    profile.save()
                    return Response({"success" : True}, status=status.HTTP_200_OK)
            else:
                return Response({"success" : False, "error" : "account_not_exists"}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "error" : "account_not_exists"}, status=status.HTTP_200_OK)

class ChangePhone(APIView):
    def post(self, request, format='json'):
        profile = None
        try:
            profile = Profile.objects.get(tel=request.data['tel'], is_hidden=False)
        except Exception as e:
            print(e)

        if profile is None:
            try:
                profile = Profile.objects.get(tel = "+" + request.data['tel'], is_hidden=False)
            except Exception as e:
                print(e)

        if profile:
            user = None
            try:
                user = User.objects.get(id = profile.user_id)
            except Exception as e:
                print(e)
            if user:
                    user.username = request.data['code'] + request.data['phone']
                    user.save()

                    profile.tel = request.data['phone']
                    profile.tel_code = request.data['code']
                    profile.save()
                    return Response({"success" : True}, status=status.HTTP_200_OK)
            else:
                return Response({"success" : False, "error" : "account_not_exists"}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "error" : "account_not_exists"}, status=status.HTTP_200_OK)

class CheckPhone(APIView):
    def post(self, request, format='json'):
        profile = None
        try:
            profile = Profile.objects.get(tel=request.data['tel'], tel_code=request.data['tel_code'], is_hidden=False)
        except Exception as e:
            print(e)

        if profile is None:
            return Response({"success" : True}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "error" : "phone_exists"}, status=status.HTTP_200_OK)

class AppConfig(APIView):
    def post(self, request, format='json'):
        return Response({"success" : True}, status=status.HTTP_200_OK)

class ProductList(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        profile = None
        try:
            profile = Profile.objects.get(id=5)
        except Exception as e:
            print(e)
        profileSerializer = ProfileSerializer(profile, context=getContext())
        products = Product.objects.filter(user=userId)
        productSerializer = ProductSerializer(products, many=True, context=getContext())
        return Response({"success" : True, "products" : productSerializer.data}, status=status.HTTP_200_OK)

class OrderList(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        orders = Order.objects.filter(purchaser=userId, is_hidden=False)
        orderSerializer = OrderSerializer(orders, many=True, context=getContext())
        updateOrders = []
        for order in orderSerializer.data:
            # order['seller'] = getObject(order['seller'])
            updateOrders.append(order)
        return Response({"success" : True, "orders" : updateOrders}, status=status.HTTP_200_OK)

class OrderProductList(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        orders = Order.objects.filter(purchaser=userId, is_hidden=False)
        orderProducts = OrderProduct.objects.filter(order__in=orders, is_hidden=False)
        orderProductSerializer = OrderProductSerializer(orderProducts, many=True, context=getContext())
        # janCodes = ProductJancode.objects.filter(id__in=orderProducts).values_list('horizontal_id', flat=True)
        # productVarietySelections = ProductVarietySelection.objects.filter(id__in=janCodes).values_list('product_variety_id', flat=True)
        # productVarieties = ProductVariety.objects.filter(id__in=productVarietySelections).values_list('product_id', flat=True)
        # products = Product.objects.filter(id__in=productVarieties)
        # productSerializer = ProductSerializer(products, many=True, context=getContext())

        return Response({"success" : True, "orderProducts" : orderProductSerializer.data}, status=status.HTTP_200_OK)

class SaleProductList(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        orders = Order.objects.filter(seller=userId, is_hidden=False).values_list('id', flat=True)
        orderProducts = OrderProduct.objects.filter(order__in=orders, is_hidden=False)
        orderProductSerializer = OrderProductSerializer(orderProducts, many=True, context=getContext())
        # janCodes = ProductJancode.objects.filter(id__in=orderProducts).values_list('horizontal_id', flat=True)
        # productVarietySelections = ProductVarietySelection.objects.filter(id__in=janCodes).values_list('product_variety_id', flat=True)
        # productVarieties = ProductVariety.objects.filter(id__in=productVarietySelections).values_list('product_id', flat=True)
        # products = Product.objects.filter(id__in=productVarieties)
        # productSerializer = ProductSerializer(products, many=True, context=getContext())
        return Response({"success" : True, "saleProducts" : orderProductSerializer.data}, status=status.HTTP_200_OK)

class CommissionProductList(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        profile = Profile.objects.get(pk=userId)
        orders = Order.objects.filter(is_hidden=False).values_list('id', flat=True)
        orderProducts = OrderProduct.objects.filter(order__in=orders, is_hidden=False).values_list('id', flat=True)
        if profile.authority_id == AUTHORITY_TYPE['MASTER']:
            orderProductsCommission = OrderProductCommission.objects.filter(user__authority_id=AUTHORITY_TYPE['MASTER'], order_product__in=orderProducts, is_hidden=False)
        else:
            orderProductsCommission = OrderProductCommission.objects.filter(user_id=userId, order_product__in=orderProducts, is_hidden=False)
        orderProductsCommissionSerializer = OrderProductCommissionSerializer(orderProductsCommission, many=True, context=getContext())
        # janCodes = ProductJancode.objects.filter(id__in=orderProducts).values_list('horizontal_id', flat=True)
        # productVarietySelections = ProductVarietySelection.objects.filter(id__in=janCodes).values_list('product_variety_id', flat=True)
        # productVarieties = ProductVariety.objects.filter(id__in=productVarietySelections).values_list('product_id', flat=True)
        # products = Product.objects.filter(id__in=productVarieties)
        # productSerializer = ProductSerializer(products, many=True, context=getContext())
        return Response({"success" : True, "commissionProducts" : orderProductsCommissionSerializer.data}, status=status.HTTP_200_OK)

class AddressList(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        addresses = Address.objects.filter(user=userId, is_hidden=False)
        addressSerializer = AddressSerializer(addresses, many=True, context=getContext())
        updatedAddress = []
        for address in addressSerializer.data:
            # address['prefecture'] = getObject(address['prefecture'])
            updatedAddress.append(address)
        return Response({"success" : True, "addresses" : updatedAddress}, status=status.HTTP_200_OK)

class CustomerList(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        profiles = Profile.objects.filter(introducer_id=userId, is_hidden=False)
        profileSerializer = ProfileSerializer(profiles, many=True, context=getContext())
        return Response({"success" : True, "customers" : profileSerializer.data}, status=status.HTTP_200_OK)

class FinancialAccountGet(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        financialAccount = FinancialAccount.objects.filter(user=userId, is_hidden=False)
        if len(financialAccount) > 0:
            financialAccount = financialAccount[0]
        else:
            financialAccount = FinancialAccount()
        financialAccountSerialier = FinancialAccountSerialier(financialAccount, context=getContext())
        return Response({"success" : True, "financialAccount" : financialAccountSerialier.data}, status=status.HTTP_200_OK)

class ProductByIds(APIView):
    serializer_class = ProductSerializer

    def get(self, request, format='json'):
        products = Product.objects.filter(id__in=request.GET.getlist('ids[]'), is_hidden=False)
        productSerializer = ProductSerializer(products, many=True, context=getContext())
        return Response({"success" : True, "products" : productSerializer.data}, status=status.HTTP_200_OK)

class UserByIds(APIView):
    serializer_class = ProductSerializer

    def get(self, request, format='json'):
        try:
            profiles = []
            ids = request.GET.getlist('ids[]')
            if 'type' in request.GET and request.GET['type'] == 'contact':
                if 'userId' in request.GET and request.GET['userId']:
                    profile = Profile.objects.get(id=request.GET['userId'], is_hidden=False)
                    sProfileSerializer = ProfileSerializer(profile, context=getContext())

                    masters = Profile.objects.filter(is_master=1)
                    ids.extend(masters.values_list('id', flat=True))

                    if sProfileSerializer.data['authority']['id'] == 1:
                        profiles = Profile.objects.filter(is_hidden=False)
                        ids.extend(Profile.objects.filter(is_hidden=False).values_list('id', flat=True))
                    elif sProfileSerializer.data['introducer'] is not None:
                        introducers = sProfileSerializer.data['introducer'].split("/")
                        introducer = introducers[len(introducers)-2]
                        ids.append(introducer)
                        ids.extend(Profile.objects.filter(introducer_id=sProfileSerializer.data['id'], is_hidden=False).values_list('id', flat=True))


            profiles = Profile.objects.filter(id__in=ids, is_hidden=False)
            if len(profiles) == 0:
                return Response({"success" : True, "users" : profiles}, status=status.HTTP_200_OK)

            profileSerializer = ProfileSerializer(profiles, many=True, context=getContext())
            return Response({"success" : True, "users" : profileSerializer.data, "data" : request.GET}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success" : False, "error": str(e)}, status=status.HTTP_200_OK)


def calculateCommission(kinujo_product, price, orderProduct, userId, shipping_fee, remaining_amount, seller):
    try:
        tax_rate = TaxRate.objects.filter(is_hidden=False, is_enable=True, end_date__isnull=True).last().tax_rate
    except:
        tax_rate = 0
    try:
        introducer = None
        profile = Profile.objects.filter(is_hidden=False, id=userId)
        if profile.exists():
            profile = profile.last()
            introducer = profile.introducer_id
        # profileSerializer = ProfileSerializer(profile, context=getContext())
        # if profileSerializer.data['introducer']:
        #     introducers = profileSerializer.data['introducer'].split("/")
        #     introducer = introducers[len(introducers)-2]
        
        if introducer:
            introducer = Profile.objects.filter(is_hidden=False, id=introducer)
            if introducer.exists():
                introducer = introducer.last()
        if introducer and introducer.authority_id != AUTHORITY_TYPE['MASTER']:
            introducerSerializer = ProfileSerializer(introducer, context=getContext())
            if kinujo_product:
                commission = introducer.authority.official_commission_rate
            else:
                commission = introducer.authority.commission_rate
            if float(commission) > 0:
                amount = int(float(price) * float(commission))
                orderProductComm = {
                    'amount' : int(amount),
                    'is_sales' : 0,
                    'is_food' : 0,
                    'shipping_fee' : 0,
                    'order_product' : orderProduct,
                    'user' : introducerSerializer.data['url']
                }
                orderProductCommissionSerializer = InsertOrderProductCommissionSerializer(data=orderProductComm, context=getContext())

                if orderProductCommissionSerializer.is_valid():
                    orderProductCommissionSerializer.save()
                else:
                    return orderProductCommissionSerializer.errors
                tax = int(float(amount) * float(tax_rate))
                result = updateUserCommission(introducer, amount, tax)
                # new remaining_amount   
                remaining_amount = int(remaining_amount) - int(float(price) * float(commission))
                return calculateCommission(kinujo_product, price, orderProduct, introducer.id, shipping_fee, remaining_amount, seller)
                
                
            return calculateCommission(kinujo_product, price, orderProduct, introducer.id, shipping_fee, remaining_amount, seller)
        else:
            if remaining_amount > 0:
                if not kinujo_product:
                    seller_commission = 0.65
                    seller_amount = int(float(price) * float(seller_commission))
                    remaining_amount = int(remaining_amount) - int(seller_amount)
                    sellerSerializer = ProfileSerializer(seller, context=getContext())
                    orderProductComm = {
                        'amount' : int(seller_amount),
                        'is_sales' : 1,
                        'is_food' : 0,
                        'shipping_fee' : int(float(shipping_fee)),
                        'order_product' : orderProduct,
                        'user' : sellerSerializer.data['url']
                    }
                    orderProductCommissionSerializer = InsertOrderProductCommissionSerializer(data=orderProductComm, context=getContext())

                    if orderProductCommissionSerializer.is_valid():
                        orderProductCommissionSerializer.save()
                    else:
                        return orderProductCommissionSerializer.errors
                    # # seller Sale
                    tax = int(float(seller_amount) * float(tax_rate))
                    result = updateUserSales(seller, seller_amount, tax, float(shipping_fee))

                    if remaining_amount > 0:
                        master_user = Profile.objects.filter(is_hidden=False, is_master=True, 
                                authority_id=AUTHORITY_TYPE['MASTER']).first()
                        if master_user:
                            sellerSerializer = ProfileSerializer(master_user, context=getContext())
                            orderProductComm = {
                                'amount' : int(remaining_amount),
                                'is_sales' : 0,
                                'is_food' : 0,
                                'shipping_fee' : 0,
                                'order_product' : orderProduct,
                                'user' : sellerSerializer.data['url']
                            }
                            orderProductCommissionSerializer = InsertOrderProductCommissionSerializer(data=orderProductComm, context=getContext())

                            if orderProductCommissionSerializer.is_valid():
                                orderProductCommissionSerializer.save()
                                # master commission
                                tax = int(float(remaining_amount) * float(tax_rate))
                                result = updateUserCommission(master_user, remaining_amount, tax)
                            else:
                                return orderProductCommissionSerializer.errors
                else:
                    sellerSerializer = ProfileSerializer(seller, context=getContext())
                    orderProductComm = {
                        'amount' : int(remaining_amount),
                        'is_sales' : 1,
                        'is_food' : 0,
                        'shipping_fee' : int(float(shipping_fee)),
                        'order_product' : orderProduct,
                        'user' : sellerSerializer.data['url']
                    }
                    orderProductCommissionSerializer = InsertOrderProductCommissionSerializer(data=orderProductComm, context=getContext())

                    if orderProductCommissionSerializer.is_valid():
                        orderProductCommissionSerializer.save()
                    else:
                        return orderProductCommissionSerializer.errors
                    # # Master Sale
                    tax = int(float(remaining_amount) * float(tax_rate))
                    result = updateUserSales(seller, remaining_amount, tax, float(shipping_fee))

    except Exception as e:
        print('calculateCommission', e)

    return ''

def updateUserCommission(introducer, amount, tax):
    today_date = date.today()
    year = today_date.year
    month = today_date.month

    totalComm = TotalCommission.objects.filter(is_hidden=False, year=year, month=month, authority=introducer.authority_id)
    if totalComm.exists():
        totalComm = totalComm.last()
    else:
        totalComm = TotalCommission()
    totalComm.order_count = int(totalComm.order_count) + 1 if totalComm.order_count else 1
    totalComm.amount = int(totalComm.amount) + int(amount) if totalComm.amount else int(amount)
    totalComm.year = year
    totalComm.month = month
    totalComm.authority_id = introducer.authority_id
    totalComm.modified = today_date
    totalComm.save()


    userCommission = UserCommision.objects.filter(is_hidden=False, year=year, month=month, user_id=introducer.id)
    if userCommission.exists():
        userCommission = userCommission.last()
    else:
        userCommission = UserCommision()
    userCommission.order_count = int(userCommission.order_count) + 1 if userCommission.order_count else 1
    userCommission.amount = int(userCommission.amount) + int(amount) if userCommission.amount else int(amount)
    userCommission.tax = int(userCommission.tax) + int(tax) if userCommission.tax else int(tax)
    userCommission.total_amount = int(userCommission.total_amount) + int(tax) + int(amount) \
        if userCommission.total_amount else int(tax) + int(amount)
    userCommission.year = year
    userCommission.month = month
    userCommission.user_id = introducer.id
    userCommission.modified = today_date
    userCommission.save()
    
    
    monthlyPayment = MonthlyPayment.objects.filter(is_hidden=False, year=year, month=month, user_id=introducer.id)
    if monthlyPayment.exists():
        monthlyPayment = monthlyPayment.last()
    else:
        monthlyPayment = MonthlyPayment()
    monthlyPayment.amount = int(monthlyPayment.amount) + int(amount) + int(tax) \
        if monthlyPayment.amount else int(amount) + int(tax)
    monthlyPayment.year = year
    monthlyPayment.month = month
    monthlyPayment.paid_date = None
    monthlyPayment.status = False
    monthlyPayment.user_id = introducer.id
    monthlyPayment.modified = today_date
    monthlyPayment.save()
    
    return True


def updateUserSales(seller, seller_amount, tax, shipping_fee):
    today_date = date.today()
    year = today_date.year
    month = today_date.month

    totalSale = TotalSale.objects.filter(is_hidden=False, year=year, month=month)
    if totalSale.exists():
        totalSale = totalSale.last()
    else:
        totalSale = TotalSale()
    totalSale.sales_amount = int(totalSale.sales_amount) + int(seller_amount) \
        if totalSale.sales_amount else int(seller_amount)
    totalSale.tax = int(totalSale.tax) + int(tax) if totalSale.tax else int(tax)
    totalSale.amount_tax_included = int(totalSale.amount_tax_included) + int(tax) + int(seller_amount) \
        if totalSale.amount_tax_included else int(tax) + int(seller_amount)
    totalSale.shipping_fee = int(totalSale.shipping_fee) + int(float(shipping_fee)) \
        if totalSale.shipping_fee else int(float(shipping_fee))
    totalSale.total_amount = int(totalSale.total_amount) + int(tax) + int(seller_amount) + int(float(shipping_fee)) \
        if totalSale.total_amount else int(tax) + int(seller_amount) + int(float(shipping_fee))
    totalSale.order_count = int(totalSale.order_count) + 1 if totalSale.order_count else 1
    totalSale.year = year
    totalSale.month = month
    totalSale.modified = today_date
    totalSale.save()

    
    userSale = UserSale.objects.filter(is_hidden=False, year=year, month=month, user_id=seller.id)
    if userSale.exists():
        userSale = userSale.last()
    else:
        userSale = UserSale()
    userSale.order_count = int(userSale.order_count)+ 1 if userSale.order_count else 1
    userSale.sales_amount = int(userSale.sales_amount) + int(seller_amount) \
        if userSale.sales_amount else int(seller_amount)
    userSale.tax = int(userSale.tax) + tax if userSale.tax else tax
    userSale.amount_tax_included = int(userSale.amount_tax_included) + int(tax) + int(seller_amount) \
        if userSale.amount_tax_included else int(tax) + int(seller_amount)
    userSale.shipping_fee = int(userSale.shipping_fee) + int(float(shipping_fee)) \
        if userSale.shipping_fee else int(float(shipping_fee))
    userSale.total_amount = int(userSale.total_amount) + int(tax) + int(seller_amount) + int(float(shipping_fee)) \
        if userSale.total_amount else int(tax) + int(seller_amount) + int(float(shipping_fee))
    userSale.user_id = seller.id
    userSale.year = year
    userSale.month = month
    userSale.modified = today_date
    userSale.save()

    
    monthlyPayment = MonthlyPayment.objects.filter(is_hidden=False, year=year, month=month, user_id=seller.id)
    if monthlyPayment.exists():
        monthlyPayment = monthlyPayment.last()
    else:
        monthlyPayment = MonthlyPayment()
    monthlyPayment.amount = int(monthlyPayment.amount) + int(tax) + int(seller_amount) + int(float(shipping_fee)) \
        if monthlyPayment.amount else int(tax) + int(seller_amount) + int(float(shipping_fee))
    monthlyPayment.user_id = seller.id
    monthlyPayment.year = year
    monthlyPayment.month = month
    monthlyPayment.modified = today_date
    monthlyPayment.paid_date = None
    monthlyPayment.status = False
    monthlyPayment.save()
    
    return True


class ProductJanCodes(APIView):
    def get(self, request, productId, format='json'):
        productVarieties = ProductVariety.objects.filter(product_id=productId, is_hidden=False).values_list('id', flat=True)
        productVarietySelections = ProductVarietySelection.objects.filter(product_variety_id__in=productVarieties, is_hidden=False).values_list('id', flat=True)
        horizontal = ProductJancode.objects.filter(horizontal_id__in=productVarietySelections, is_hidden=False)
        vertical = ProductJancode.objects.filter(vertical_id__in=productVarietySelections, is_hidden=False)
        horizontalSerializer = ProductJancodeSerializer(horizontal, many=True, context=getContext())
        verticalSerializer = ProductJancodeSerializer(vertical, many=True, context=getContext())
        return Response({"success" : True, "verticals" : verticalSerializer.data, "horizontals" : horizontalSerializer.data}, status=status.HTTP_200_OK)

class RemoveReferral(APIView):
    def post(self, request, format='json'):
        user = request.data['userId']
        parent = request.data['parentId']
        profiles = Profile.objects.filter(id=user, is_hidden=False).filter(introducer_id=parent)
        profile = profiles[0]
        profile.introducer = None
        profile.save()
        return Response({"success" : True}, status=status.HTTP_200_OK)

class OrderReceipt(APIView):
    def post(self, request, orderId, format='json'):
        user = request.data['userId']
        parent = request.data['parentId']
        profiles = Profile.objects.filter(id=user, is_hidden=False).filter(introducer_id=parent)
        profile = profiles[0]
        profile.introducer = None
        profile.save()
        return Response({"success" : True}, status=status.HTTP_200_OK)

class Pay(APIView):
    def post(self, request, userId, format='json'):
        stripe.api_key = "sk_test_siDHJkaiXknooQGf1pStMNWY"
        try:
            body = json.loads(request.body)
            if(len(body['products']) == 0):
                return Response({"success" : False, "errors": {"no_products" : "No products"}}, status=status.HTTP_200_OK)

            # token = stripe.Token.create(
            #     card={
            #         "number": request.data['card']['number'].replace(" ", ""),
            #         "exp_month": request.data['card']['expiry'].split("/")[0],
            #         "exp_year": "20" + request.data['card']['expiry'].split("/")[1],
            #         "cvc": request.data['card']['cvc'],
            #     },
            # )
            sellers = []
            profile = Profile.objects.get(id=userId, is_hidden=False)
            tax = TaxRate.objects.get(id=body['tax'], is_hidden=False)
            customer_id = None

            ids = []
            quantities = {}
            varieties = {}

            for product in body['products']:
                # quantities['item_' + str(product['product_id'])] = product['quantity']
                # varieties['item_' + str(product['product_id'])] = product['varietyId']
                # ids.append(product['product_id'])
                quantities['item_' + str(product[0][1])] = product[0][3]
                varieties['item_' + str(product[0][1])] = product[0][2]
                ids.append(product[0][1])

            products = Product.objects.filter(id__in=ids)
            address = Address.objects.get(id=body['address'])

            groupProducts = {}
            orderIds = []

            if products and profile and address:
                profileSerializer = ProfileSerializer(profile, context=getContext())
                productSerializer = ProductSerializer(products, many=True, context=getContext())
                addressSerializer = AddressSerializer(address, context=getContext())

                amount = total_amount = total_tax = total_shipping_fee = 0
                seller = None
                product_name = ''
                one_product = ''

                for product in productSerializer.data:
                    seller = Profile.objects.get(pk=product['user']['id'])
                    one_product = product
                    product_name = product['name']
                    quantity = quantities['item_' + str(product['id'])]
                    if profileSerializer.data['is_seller']:
                        amount = int(float(amount) + (float(product['store_price']) * float(quantity)))
                    else:
                        amount = int(float(amount) + (float(product['price']) * float(quantity)))
                    total_tax = int(total_tax) + int(float(amount) * float(tax.tax_rate))
                    total_shipping_fee = int(float(total_shipping_fee) + float(product['shipping_fee']))

                    # if product['user']['url'] in groupProducts:
                    #     tmpProducts = groupProducts[product['user']['url']]
                    #     tmpProducts.append(product)
                    #     groupProducts[product['user']['url']] = tmpProducts
                    # else:
                    #     groupProducts[product['user']['url']] = [product]
                
                total_amount = int(amount) + int(total_shipping_fee)
                # charge = stripe.Charge.create(
                #     amount=int(float(total_amount)),
                #     currency="jpy",
                #     source=token_id,
                #     description="Order by " + str(profileSerializer.data['id']),
                # )

                address2 = addressSerializer.data['address2']
                if address2 is None:
                    address2 = "no_address_2"

                order = {
                    'amount' : amount,
                    'tax': total_tax,
                    'shipping_fee': total_shipping_fee,
                    'shipped_date': None,
                    'total_amount': total_amount + total_tax,
                    'name': addressSerializer.data['name'],
                    'zip1': addressSerializer.data['zip1'],
                    'tel_code': addressSerializer.data['tel_code'],
                    'address1': addressSerializer.data['address1'],
                    'address2': address2,
                    'tel': addressSerializer.data['tel'],
                    'is_hidden': 0,
                    'prefecture': addressSerializer.data['prefecture']['url'],
                    'seller': one_product['user']['url'],
                    'purchaser' : profileSerializer.data['url'],
                    'status' : 1
                }
                orderSerializer = InsertOrderSerializer(data=order, context=getContext())
                if orderSerializer.is_valid():
                    newOrder = orderSerializer.save()
                    shop_name = ""
                    if seller.shop_name:
                        shop_name = seller.shop_name
                    elif seller.real_name:
                        shop_name = seller.real_name
                    elif seller.nickname:
                        shop_name = seller.nickname

                    orderReceipt = {
                        'is_copy' : 0,
                        'to_name' : addressSerializer.data['name'],
                        'amount' : total_amount,
                        'output_date' : date.today(),
                        'order_date' : date.today(),
                        'product_name' : product_name,
                        'shop_name' : shop_name,
                        'address' : addressSerializer.data['address1'],
                        'order' : orderSerializer.data['url'],
                        'payment' : body['checkoutSessionId']
                    }
                    orderReceiptSerializer = OrderReceiptSerializer(data=orderReceipt, context=getContext())
                    if orderReceiptSerializer.is_valid():
                        orderReceiptSerializer.save()
                    else:
                        return Response({"success" : False, "errors" : orderReceiptSerializer.errors}, status=status.HTTP_200_OK)

                    kinujo_product = if_kinujo_product(seller.id)
                    for product in productSerializer.data:
                        quantity = quantities['item_' + str(product['id'])]
                        price = 0
                        groupTotal = 0
                        groupShippingFee = float(product['shipping_fee'])

                        if profileSerializer.data['is_seller']:
                            price= float(product['store_price'])
                            groupTotal = int(float(product['store_price']) * float(quantity))
                        else:
                            price= float(product['price'])
                            groupTotal = int(float(product['price']) * float(quantity))
                        groupTax = int(float(groupTotal) * float(tax.tax_rate))

                        varietyId = varieties['item_' + str(product['id'])]

                        variety = None
                        variety = ProductJancode.objects.get(id=varietyId)
                        varietySerializer = ProductJancodeSerializer(variety, context=getContext())
                        variety = varietySerializer.data['url']

                        orderIds.append(orderSerializer.data['id'])

                        orderProduct = {
                            'quantity':  quantity,
                            'unit_price' : int(price),
                            'total_price' : groupTotal,
                            'tax': groupTax,
                            'total_amount': groupTotal + groupTax,
                            'order': orderSerializer.data['url'],
                            'product_jan_code': variety
                        }
                        orderProductSerializer = InsertOrderProductSerializer(data=orderProduct, context=getContext())
                        if orderProductSerializer.is_valid():
                            orderProductSerializer.save()

                            productJancode = ProductJancode.objects.get(id=varietyId)
                            if productJancode:
                                productJancode.stock = int(productJancode.stock) - int(quantity)
                                productJancode.save()

                            errors = calculateCommission(kinujo_product, groupTotal, orderProductSerializer.data['url'], 
                                        profileSerializer.data['id'], groupShippingFee, groupTotal, seller)
                            if errors:
                                return Response({"success" : False, "errors" : errors}, status=status.HTTP_200_OK)
                        else:
                            return Response({"success" : False, "errors" : orderProductSerializer.errors}, status=status.HTTP_200_OK)

                        if product['user']['email']:
                            send_mail(
                                '[KINUJOからのお知らせ」出品中の商品が購入されました',
                                'いつもKINUJOをご利用いただきありがとうございます。' + "<br><br>" +
                                '出品中の下記の商品が購入されまUた。' +  "<br>" +
                                '商品の発送をお願いいたします。' + "<br><br>" +
                                '商品情報' + "<br>" +
                                'オーダーID:' + str(orderSerializer.data['id']) + "<br>" +
                                '商品名:' + product['name'] + "<br>" +
                                '商品価格:' + str(float(groupTotal)) + "<br>" +
                                '購入者様:' + addressSerializer.data['name'] + "<br>" + "<br>" +
                                '発送を終えたら' + "<br>" +
                                '管理サイトから注文の状態を発送完了に変更し、発送日とお問い合わせ番号を入力Uて更新Uてください。' + "<br>" +
                                '発送した日、配送方法やお問い合わせ番号をチャットでお伝えいただくと、購入者様も喜ばれます。' + "<br><br>" +
                                "お問い合わせは、アプリ内のチャットをご利用＜ださい。",
                                'support@kinujo.app',
                                [product['user']['email']],
                                fail_silently=False,
                            )

                        sellers.append(product['user']['id'])
                else:
                    return Response({"success" : False, "errors" : orderSerializer.errors}, status=status.HTTP_200_OK)

            else:
                return Response({"success" : False, "errors": ["Invalid data."]}, status=status.HTTP_200_OK)
            # if profile:
            #     profileSerializer = ProfileSerializer(profile, context=getContext())
            #     payload = profileSerializer.data['payload']
            #     payload = payload.replace("'", '"')
            #     if payload and payload is not None:
            #         payload = payload.replace("'", '"')
            #         payload = ast.literal_eval(payload)

            #     if  payload and payload is not None and 'customerId' in payload:
            #         customer_id = payload["customerId"]
            #     else:
            #         customer = stripe.Customer.create(
            #             description=profileSerializer.data['id'],
            #         )
            #         customer_id = customer.id

            #         payload["customerId"] = customer_id
            #         profile.payload = json.dumps(payload)
            #         profile.save()

            return Response({"success" : True, "sellers" : sellers})
        except Exception as e:
            print('error', e)
            return Response({"success" : False, "error": str(e)}, status=status.HTTP_200_OK)

class UpdateProfileImage(APIView):
    def post(self, request, userId, format='json'):
        profile = Profile.objects.get(id=userId, is_hidden=False)
        image = Image.objects.get(id=request.data['image_id'])
        if request.data['type'] == 'image':
            profile.image = image
        if request.data['type'] == 'background_img':
            profile.background_img = image
        profile.save()
        return Response({"success" : True}, status=status.HTTP_200_OK)

class CreateProduct(APIView):
    def post(self, request, userId, format='json'):
        try:
            if request.data['draft'] != 1:
                if request.data['productName'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in product name."]}, status=status.HTTP_200_OK)
                if request.data['brandName'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in brand name."]}, status=status.HTTP_200_OK)
                if request.data['pr'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in PR statement."]}, status=status.HTTP_200_OK)
                if request.data['productId'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in product ID."]}, status=status.HTTP_200_OK)
                if request.data['productCategory'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in product category."]}, status=status.HTTP_200_OK)
                if request.data['productVariation'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in product variation."]}, status=status.HTTP_200_OK)
                if request.data['publishState'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in publish state."]}, status=status.HTTP_200_OK)
                if request.data['publishDate'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in publish date."]}, status=status.HTTP_200_OK)
                if request.data['price'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in price."]}, status=status.HTTP_200_OK)
                if request.data['storePrice'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in store price."]}, status=status.HTTP_200_OK)
                if request.data['shipping'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in shipping."]}, status=status.HTTP_200_OK)
                if request.data['productPageDisplayMethod'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in product page display method."]}, status=status.HTTP_200_OK)
                if request.data['productDescription'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in product description."]}, status=status.HTTP_200_OK)

            variety = 0

            if request.data['productVariation'] == 'none':
                if request.data['draft'] != 1:
                    noneVariationItems = request.data['noneVariationItems']
                    if not noneVariationItems:
                        noneVariationItems = {'janCode': "", 'stock': 0}
                    if noneVariationItems['janCode'] == "" and 'delete' in noneVariationItems and not noneVariationItems['delete']:
                        return Response({"success" : False, "errors" : ["Please fill in Jan Code."]}, status=status.HTTP_200_OK)
                    if noneVariationItems['stock'] == "" and 'delete' in noneVariationItems and not noneVariationItems['delete']:
                        return Response({"success" : False, "errors" : ["Please fill in stock."]}, status=status.HTTP_200_OK)
                variety = 0
            if request.data['productVariation'] == 'one':
                if request.data['draft'] != 1:
                    oneVariationItems = request.data['oneVariationItems']
                    for item in oneVariationItems['items']:
                        if item['janCode'] == "" and 'delete' in item and not item['delete']:
                            return Response({"success" : False, "errors" : ["Please fill in Jan Code."]}, status=status.HTTP_200_OK)
                        if item['stock'] == "" and 'delete' in item and not item['delete']:
                            return Response({"success" : False, "errors" : ["Please fill in stock."]}, status=status.HTTP_200_OK)
                variety = 1
            if request.data['productVariation'] == 'two':
                if request.data['draft'] != 1:
                    twoVariationItems = request.data['twoVariationItems']
                    mappingValues = twoVariationItems['mappingValue']
                    firstItem = twoVariationItems['items'][0]
                    secondItem = twoVariationItems['items'][1]
                    for choice1 in firstItem['choices']:
                        for choice2 in secondItem['choices']:
                            if mappingValues[choice1['choiceItem']][choice2['choiceItem']]['janCode'] == "" and 'delete' in mappingValues[choice1['choiceItem']][choice2['choiceItem']] and not mappingValues[choice1['choiceItem']][choice2['choiceItem']]['delete']:
                                return Response({"success" : False, "errors" : ["Please fill in Jan Code."]}, status=status.HTTP_200_OK)
                            if mappingValues[choice1['choiceItem']][choice2['choiceItem']]['stock'] == "" and 'delete' in mappingValues[choice1['choiceItem']][choice2['choiceItem']] and not mappingValues[choice1['choiceItem']][choice2['choiceItem']]['delete']:
                                return Response({"success" : False, "errors" : ["Please fill in stock."]}, status=status.HTTP_200_OK)
                variety = 2

            profile = Profile.objects.get(id=userId, is_hidden=False)
            profileSerializer = ProfileSerializer(profile, context=getContext())

            productData = {
                "name" : request.data['productName'],
                "brand_name" : request.data["brandName"],
                "pr" : request.data["pr"],
                "url_str" : request.data['productId'],
                "variety" : variety,
                "opened_date" : request.data['publishDate'],
                "price" : 0 if request.data['price'] == '' or request.data['price'] == None else request.data['price'],
                "store_price" : 0 if request.data['storePrice'] == '' or request.data['storePrice'] == None else request.data['storePrice'],
                "shipping_fee": 0 if request.data['shipping'] == '' or request.data['shipping'] == None else request.data['shipping'],
                "description" : request.data['productDescription'],
                "category" : request.data['productCategory'],
                "user" : profileSerializer.data['url']
            }
            if request.data['draft'] == 1:
                productData['is_draft'] = 1
                productData['opened_date'] = None
            else:
                productData['is_draft'] = 0
            if request.data['publishState'] == 'published':
                productData['is_opened'] = 1
            else:
                productData['is_opened'] = 0

            if request.data['publishState'] == 'published':
                productData['is_opened'] = 1
            else:
                productData['is_opened'] = 0

            if request.data['productStatus'] == 'new':
                productData['is_used'] = 0
            else:
                productData['is_used'] = 1

            if request.data['targetUser'] == 'allUser':
                productData['target'] = 0
            elif request.data['targetUser'] == 'generalUser':
                productData['target'] = 1
            elif request.data['targetUser'] == 'storeUser':
                productData['target'] = 2

            productSerializer = InsertProductSerializer(data=productData, context=getContext())
            if productSerializer.is_valid():
                productSerializer.save()
                productImages = request.data['productImages']
                for productImage in productImages:
                    productImageSerializer = InsertProductImageSerializer(data={
                        'image': productImage['url'],
                        'product' : productSerializer.data['url']
                    }, context=getContext())
                    if productImageSerializer.is_valid():
                        productImageSerializer.save()
                    else:
                        return Response({"success" : False, "errors": productImageSerializer.errors}, status=status.HTTP_200_OK)

                if request.data['productVariation'] == 'none':
                    noneVariationItems = request.data['noneVariationItems']
                    if not noneVariationItems:
                        noneVariationItems = {'janCode': "", 'stock': 0}
                    insertProductVarietySerializer = InsertProductVarietySerializer(data={
                        "name" : "none",
                        "product" : productSerializer.data['url'],
                        "vertical_and_horizontal" : 0
                    }, context=getContext())
                    if insertProductVarietySerializer.is_valid():
                        insertProductVarietySerializer.save()
                        insertProductVarietySelectionSerializer = InsertProductVarietySelectionSerializer(data={
                            "selection" : "none",
                            "product_variety" : insertProductVarietySerializer.data['url']
                        }, context=getContext())
                        if insertProductVarietySelectionSerializer.is_valid():
                            insertProductVarietySelectionSerializer.save()
                            insertProductJancodeSerializer = InsertProductJancodeSerializer(data={
                                "jan_code" : noneVariationItems['janCode'],
                                "stock" : noneVariationItems['stock'],
                                "horizontal" : insertProductVarietySelectionSerializer.data['url']
                            }, context=getContext())
                            if insertProductJancodeSerializer.is_valid():
                                insertProductJancodeSerializer.save()
                            else:
                                return Response({"success" : False, "errors": insertProductJancodeSerializer.errors}, status=status.HTTP_200_OK)
                        else:
                            return Response({"success" : False, "errors": insertProductVarietySelectionSerializer.errors}, status=status.HTTP_200_OK)
                    else:
                        return Response({"success" : False, "errors": insertProductVarietySerializer.errors}, status=status.HTTP_200_OK)
                elif request.data['productVariation'] == 'one':
                    oneVariationItems = request.data['oneVariationItems']
                    insertProductVarietySerializer = InsertProductVarietySerializer(data={
                        "name" : oneVariationItems['name'],
                        "product" : productSerializer.data['url'],
                        "vertical_and_horizontal" : 0
                    }, context=getContext())
                    if insertProductVarietySerializer.is_valid():
                        insertProductVarietySerializer.save()

                        for item in oneVariationItems['items']:
                            insertProductVarietySelectionSerializer = InsertProductVarietySelectionSerializer(data={
                                "selection" : item['choice'],
                                "product_variety" : insertProductVarietySerializer.data['url']
                            }, context=getContext())
                            if insertProductVarietySelectionSerializer.is_valid():
                                insertProductVarietySelectionSerializer.save()
                                hiddenValue = 0
                                if 'delete' in item and item['delete']:
                                    hiddenValue = 1

                                insertProductJancodeSerializer = InsertProductJancodeSerializer(data={
                                    "jan_code" : item['janCode'],
                                    "stock" : item['stock'],
                                    "is_hidden" : hiddenValue,
                                    "horizontal" : insertProductVarietySelectionSerializer.data['url']
                                }, context=getContext())
                                if insertProductJancodeSerializer.is_valid():
                                    insertProductJancodeSerializer.save()
                                else:
                                    return Response({"success" : False, "errors": insertProductJancodeSerializer.errors}, status=status.HTTP_200_OK)
                            else:
                                return Response({"success" : False, "errors": insertProductVarietySelectionSerializer.errors}, status=status.HTTP_200_OK)
                    else:
                        return Response({"success" : False, "errors": insertProductVarietySerializer.errors}, status=status.HTTP_200_OK)
                elif request.data['productVariation'] == 'two':
                    twoVariationItems = request.data['twoVariationItems']
                    firstUrls = {}
                    secondUrls = {}
                    firstItem = twoVariationItems['items'][0]
                    secondItem = twoVariationItems['items'][1]

                    firstInsertProductVarietySerializer = InsertProductVarietySerializer(data={
                        "name" : firstItem['horizontalItem'],
                        "product" : productSerializer.data['url'],
                        "vertical_and_horizontal" : 1
                    }, context=getContext())
                    if firstInsertProductVarietySerializer.is_valid():
                        firstInsertProductVarietySerializer.save()
                        for choice in firstItem['choices']:
                            firstInsertProductVarietySelectionSerializer = InsertProductVarietySelectionSerializer(data={
                                "selection" : choice['choiceItem'],
                                "product_variety" : firstInsertProductVarietySerializer.data['url']
                            }, context=getContext())
                            if firstInsertProductVarietySelectionSerializer.is_valid():
                                firstInsertProductVarietySelectionSerializer.save()
                                firstUrls[choice['choiceItem']] = firstInsertProductVarietySelectionSerializer.data['url']
                            else:
                                return Response({"success" : False, "errors": firstInsertProductVarietySelectionSerializer.errors}, status=status.HTTP_200_OK)
                    else:
                        return Response({"success" : False, "errors": firstInsertProductVarietySerializer.errors}, status=status.HTTP_200_OK)

                    secondInsertProductVarietySerializer = InsertProductVarietySerializer(data={
                        "name" : secondItem['horizontalItem'],
                        "product" : productSerializer.data['url'],
                        "vertical_and_horizontal" : 1
                    }, context=getContext())
                    if secondInsertProductVarietySerializer.is_valid():
                        secondInsertProductVarietySerializer.save()
                        for choice in secondItem['choices']:
                            secondInsertProductVarietySelectionSerializer = InsertProductVarietySelectionSerializer(data={
                                "selection" : choice['choiceItem'],
                                "product_variety" : secondInsertProductVarietySerializer.data['url']
                            }, context=getContext())
                            if secondInsertProductVarietySelectionSerializer.is_valid():
                                secondInsertProductVarietySelectionSerializer.save()
                                secondUrls[choice['choiceItem']] = secondInsertProductVarietySelectionSerializer.data['url']
                            else:
                                return Response({"success" : False, "errors": secondInsertProductVarietySelectionSerializer.errors}, status=status.HTTP_200_OK)
                    else:
                        return Response({"success" : False, "errors": secondInsertProductVarietySerializer.errors}, status=status.HTTP_200_OK)

                    mappingValues = twoVariationItems['mappingValue']
                    for choice1 in firstItem['choices']:
                        for choice2 in secondItem['choices']:
                            hiddenValue = 0
                            if 'delete' in mappingValues[choice1['choiceItem']][choice2['choiceItem']] and mappingValues[choice1['choiceItem']][choice2['choiceItem']]['delete']:
                                hiddenValue = 1
                            insertProductJancodeSerializer = InsertProductJancodeSerializer(data={
                                "jan_code" : mappingValues[choice1['choiceItem']][choice2['choiceItem']]['janCode'],
                                "stock" : mappingValues[choice1['choiceItem']][choice2['choiceItem']]['stock'],
                                "is_hidden" : hiddenValue,
                                "horizontal" : firstUrls[choice1['choiceItem']],
                                "vertical" : secondUrls[choice2['choiceItem']]
                            }, context=getContext())
                            if insertProductJancodeSerializer.is_valid():
                                insertProductJancodeSerializer.save()
                            else:
                                return Response({"success" : False, "errors": insertProductJancodeSerializer.errors}, status=status.HTTP_200_OK)

            else:
                return Response({"success" : False, "errors": productSerializer.errors}, status=status.HTTP_200_OK)
            return Response({"success" : True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success" : False, "error": str(e)}, status=status.HTTP_200_OK)

class GetProductByVariety(APIView):
    def get(self, request, format='json'):
        product = Product.objects.get(id=request.GET['productId'], is_hidden=False)
        productSerializer = ProductSerializer(product, context=getContext())
        janCodes = []
        for productVariety in productSerializer.data['productVarieties']:
            for productVarietySelection in productVariety['productVarietySelections']:
                for horizontal in productVarietySelection['jancode_horizontal']:
                    janCodes.append(horizontal['jan_code'])
                for vertical in productVarietySelection['jancode_vertical']:
                    janCodes.append(vertical['jan_code'])
        productJancodes = ProductJancode.objects.filter(jan_code__in=janCodes, is_hidden=False)
        productJancodesSerializer = ProductJancodeSerializer(productJancodes, many=True, context=getContext())


        horizontals = ProductJancode.objects.filter(jan_code__in=janCodes, is_hidden=False).values_list('horizontal_id', flat=True)
        verticals = ProductJancode.objects.filter(jan_code__in=janCodes, is_hidden=False).values_list('vertical_id', flat=True)
        janCodeIds = []
        janCodeIds.extend(horizontals)
        janCodeIds.extend(verticals)
        productVarietyIDs = ProductVarietySelection.objects.filter(id__in=janCodeIds, is_hidden=False).values_list("product_variety_id", flat=True)
        productIDs = ProductVariety.objects.filter(id__in=productVarietyIDs, is_hidden=False).values_list("product_id", flat=True)
        products = Product.objects.filter(id__in=productIDs, is_hidden=False)
        productSerializer = SimpleProductSerializer(products, many=True, context=getContext())
        return Response({"success" : True, "products" : productSerializer.data}, status=status.HTTP_200_OK)


class EditProduct(APIView):
    def post(self, request, userId, format='json'):
        try:
            if request.data['draft'] != 1:
                if request.data['id'] == "":
                    return Response({"success" : False, "errors" : ["Invalid update."]}, status=status.HTTP_200_OK)
                if request.data['productName'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in product name."]}, status=status.HTTP_200_OK)
                if request.data['brandName'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in brand name."]}, status=status.HTTP_200_OK)
                if request.data['pr'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in PR statement."]}, status=status.HTTP_200_OK)
                if request.data['productId'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in product ID."]}, status=status.HTTP_200_OK)
                if request.data['productCategory'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in product category."]}, status=status.HTTP_200_OK)
                if request.data['productVariation'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in product variation."]}, status=status.HTTP_200_OK)
                if request.data['publishState'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in publish state."]}, status=status.HTTP_200_OK)
                if request.data['publishDate'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in publish date."]}, status=status.HTTP_200_OK)
                if request.data['price'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in price."]}, status=status.HTTP_200_OK)
                if request.data['storePrice'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in store price."]}, status=status.HTTP_200_OK)
                if request.data['shipping'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in shipping."]}, status=status.HTTP_200_OK)
                if request.data['productPageDisplayMethod'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in product page display method."]}, status=status.HTTP_200_OK)
                if request.data['productDescription'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in product description."]}, status=status.HTTP_200_OK)

            variety = 0

            if request.data['productVariation'] == 'none':
                if request.data['draft'] != 1:
                    noneVariationItems = request.data['noneVariationItems']
                    if not noneVariationItems:
                        noneVariationItems = {'janCode': "", 'stock': 0}
                    if noneVariationItems['janCode'] == "":
                        return Response({"success" : False, "errors" : ["Please fill in Jan Code."]}, status=status.HTTP_200_OK)
                    if noneVariationItems['stock'] == "":
                        return Response({"success" : False, "errors" : ["Please fill in stock."]}, status=status.HTTP_200_OK)
                variety = 0
            if request.data['productVariation'] == 'one':
                if request.data['draft'] != 1:
                    oneVariationItems = request.data['oneVariationItems']
                    for item in oneVariationItems['items']:
                        if item['janCode'] == "":
                            return Response({"success" : False, "errors" : ["Please fill in Jan Code."]}, status=status.HTTP_200_OK)
                        if item['stock'] == "":
                            return Response({"success" : False, "errors" : ["Please fill in stock."]}, status=status.HTTP_200_OK)
                variety = 1
            if request.data['productVariation'] == 'two':
                if request.data['draft'] != 1:
                    twoVariationItems = request.data['twoVariationItems']
                    mappingValues = twoVariationItems['mappingValue']
                    firstItem = twoVariationItems['items'][0]
                    secondItem = twoVariationItems['items'][1]
                    for choice1 in firstItem['choices']:
                        for choice2 in secondItem['choices']:
                            if mappingValues[choice1['choiceItem']][choice2['choiceItem']]['janCode'] == "":
                                return Response({"success" : False, "errors" : ["Please fill in Jan Code."]}, status=status.HTTP_200_OK)
                            if mappingValues[choice1['choiceItem']][choice2['choiceItem']]['stock'] == "":
                                return Response({"success" : False, "errors" : ["Please fill in stock."]}, status=status.HTTP_200_OK)
                variety = 2

            profile = Profile.objects.get(id=userId, is_hidden=False)
            profileSerializer = ProfileSerializer(profile, context=getContext())


            product = Product.objects.get(id=request.data['id'])
            product.name = request.data['productName']
            product.brand_name = request.data["brandName"]
            product.pr = request.data["pr"]
            product.url_str = request.data["productId"]
            product.variety = variety
            product.opened_date = request.data["publishDate"]
            product.price = 0 if request.data['price'] == '' or request.data['price'] == None else request.data['price']
            product.store_price = 0 if request.data['storePrice'] == '' or request.data['storePrice'] == None else request.data['storePrice']
            product.shipping_fee = 0 if request.data['shipping'] == '' or request.data['shipping'] == None else request.data['shipping']
            product.description = request.data["productDescription"]

            productCategories = request.data['productCategory'].split("/")
            productCategoryId = productCategories[len(productCategories)-2]
            if productCategoryId and productCategoryId != "":
                productCategory = ProductCategory.objects.get(id=productCategoryId)
            else:
                productCategory = None

            product.category = productCategory
            if request.data['draft'] == 1:
                product.is_draft = 1
                product.opened_date = None
            else:
                product.is_draft = 0
            if request.data['publishState'] == 'published':
                product.is_opened = 1
            else:
                product.is_opened = 0

            if request.data['productStatus'] == 'new':
                product.is_used = 0
            else:
                product.is_used = 1

            # if request.data['draft']:
            #     product.is_draft = 1
            # else:
            #     product.is_draft = 0

            if request.data['targetUser'] == 'allUser':
                product.target = 0
            elif request.data['targetUser'] == 'generalUser':
                product.target = 1
            elif request.data['targetUser'] == 'storeUser':
                product.target = 2
            product.save()

            productSerializer = InsertProductSerializer(product, context=getContext())
            productImages = request.data['productImages']
            for productImage in productImages:
                if 'is_old' not in productImage:
                    productImageSerializer = InsertProductImageSerializer(data={
                        'image': productImage['url'],
                        'product' : productSerializer.data['url']
                    }, context=getContext())
                    if productImageSerializer.is_valid():
                        productImageSerializer.save()
                    else:
                        return Response({"success" : False, "errors": productImageSerializer.errors}, status=status.HTTP_200_OK)

            if request.data['productVariation'] == 'none':
                noneVariationItems = request.data['noneVariationItems']
                if not noneVariationItems:
                    noneVariationItems = {'janCode': "", 'stock': 0}
                if "id" in noneVariationItems:
                    productJancode = ProductJancode.objects.get(id=noneVariationItems["id"])
                    productJancode.jan_code = noneVariationItems['janCode']
                    productJancode.stock = noneVariationItems['stock']
                    productJancode.save()
            elif request.data['productVariation'] == 'one':
                oneVariationItems = request.data['oneVariationItems']
                productVariety = ProductVariety.objects.get(id=oneVariationItems['id'])
                productVarietySerializer = ProductVarietySerializer(productVariety, context=getContext())
                productVariety.name = oneVariationItems['name']
                productVariety.save()

                for item in oneVariationItems['items']:
                    if "id" in item:
                        productJancode = ProductJancode.objects.get(id=item["id"])
                        productJancode.jan_code = item['janCode']
                        productJancode.stock = item['stock']
                        productJancode.save()

                        productVarietySelection = ProductVarietySelection.objects.get(id=productJancode.horizontal.id)
                        productVarietySelection.selection = item['choice']
                        productVarietySelection.save()
                    else:
                        productVarietySelectionSerializer = InsertProductVarietySelectionSerializer(data={
                            "selection" : item['choice'],
                            "product_variety" : productVarietySerializer.data['url']
                        }, context=getContext())
                        if productVarietySelectionSerializer.is_valid():
                            productVarietySelectionSerializer.save()

                            productJancodeSerializer = InsertProductJancodeSerializer(data={
                                "jan_code" : item['janCode'],
                                "stock" : item['stock'],
                                "is_hidden" : 0,
                                "horizontal" : productVarietySelectionSerializer.data['url']
                            }, context=getContext())
                            if productJancodeSerializer.is_valid():
                                productJancodeSerializer.save()
                            else:
                                return Response({"success" : False, "errors": productJancodeSerializer.errors}, status=status.HTTP_200_OK)
                        else:
                            return Response({"success" : False, "errors": productVarietySelectionSerializer.errors}, status=status.HTTP_200_OK)
            elif request.data['productVariation'] == 'two':
                twoVariationItems = request.data['twoVariationItems']
                mappingValues = twoVariationItems['mappingValue']
                firstItem = twoVariationItems['items'][0]
                secondItem = twoVariationItems['items'][1]

                firstProductVariety = ProductVariety.objects.get(id=firstItem['id'])
                firstProductVariety.name = firstItem['horizontalItem']
                firstProductVariety.save()
                secondProductVariety = ProductVariety.objects.get(id=secondItem['id'])
                secondProductVariety.name = firstItem['horizontalItem']
                secondProductVariety.save()

                firstInsertProductVarietySerializer = InsertProductVarietySerializer(firstProductVariety, context=getContext())
                secondInsertProductVarietySerializer = InsertProductVarietySerializer(secondProductVariety, context=getContext())

                firstUrls = {}
                secondUrls = {}
                for choice in firstItem['choices']:
                    if 'delete' in choice and choice['delete']:
                        productVarietySelection = ProductVarietySelection.objects.get(id=choice['id'])
                        productVarietySelection.is_hidden = 1
                        productVarietySelection.save()

                    if 'id' in choice:
                        productVarietySelection = ProductVarietySelection.objects.get(id=choice['id'])
                        productVarietySelection.selection = choice['choiceItem']
                        productVarietySelection.save()

                        firstInsertProductVarietySelectionSerializer = InsertProductVarietySelectionSerializer(productVarietySelection, context=getContext())
                        firstUrls[choice['choiceItem']] = firstInsertProductVarietySelectionSerializer.data['url']
                    else:
                        firstInsertProductVarietySelectionSerializer = InsertProductVarietySelectionSerializer(data={
                            "selection" : choice['choiceItem'],
                            "product_variety" : firstInsertProductVarietySerializer.data['url']
                        }, context=getContext())
                        if firstInsertProductVarietySelectionSerializer.is_valid():
                            firstInsertProductVarietySelectionSerializer.save()
                            firstUrls[choice['choiceItem']] = firstInsertProductVarietySelectionSerializer.data['url']
                        else:
                            return Response({"success" : False, "errors": firstInsertProductVarietySelectionSerializer.errors}, status=status.HTTP_200_OK)

                for choice in secondItem['choices']:
                    if 'delete' in choice and choice['delete']:
                        productVarietySelection = ProductVarietySelection.objects.get(id=choice['id'])
                        productVarietySelection.is_hidden = 1
                        productVarietySelection.save()
                        
                    if 'id' in choice:
                        productVarietySelection = ProductVarietySelection.objects.get(id=choice['id'])
                        productVarietySelection.selection = choice['choiceItem']
                        productVarietySelection.save()

                        secondInsertProductVarietySelectionSerializer = InsertProductVarietySelectionSerializer(productVarietySelection, context=getContext())
                        secondUrls[choice['choiceItem']] = secondInsertProductVarietySelectionSerializer.data['url']
                    else:
                        secondInsertProductVarietySelectionSerializer = InsertProductVarietySelectionSerializer(data={
                            "selection" : choice['choiceItem'],
                            "product_variety" : firstInsertProductVarietySerializer.data['url']
                        }, context=getContext())
                        if secondInsertProductVarietySelectionSerializer.is_valid():
                            secondInsertProductVarietySelectionSerializer.save()
                            secondUrls[choice['choiceItem']] = secondInsertProductVarietySelectionSerializer.data['url']
                        else:
                            return Response({"success" : False, "errors": secondInsertProductVarietySelectionSerializer.errors}, status=status.HTTP_200_OK)

                for choice1 in firstItem['choices']:
                    for choice2 in secondItem['choices']:
                        tmpChoice = mappingValues[choice1['choiceItem']][choice2['choiceItem']]
                        if 'id' in tmpChoice:
                            productJancode = ProductJancode.objects.get(id=tmpChoice['id'])
                            productJancode.jan_code = tmpChoice['janCode']
                            is_hidden = 0
                            if 'delete' in tmpChoice and tmpChoice['delete']:
                                is_hidden = 1
                            productJancode.jan_code = tmpChoice['janCode']
                            productJancode.is_hidden = is_hidden
                            productJancode.stock = tmpChoice['stock']
                            productJancode.save()
                        else:
                            hiddenValue = 0
                            if 'delete' in mappingValues[choice1['choiceItem']][choice2['choiceItem']]:
                                if mappingValues[choice1['choiceItem']][choice2['choiceItem']]['delete']:
                                    hiddenValue = 1
                            insertProductJancodeSerializer = InsertProductJancodeSerializer(data={
                                "jan_code" : mappingValues[choice1['choiceItem']][choice2['choiceItem']]['janCode'],
                                "stock" : mappingValues[choice1['choiceItem']][choice2['choiceItem']]['stock'],
                                "is_hidden" : hiddenValue,
                                "horizontal" : firstUrls[choice1['choiceItem']],
                                "vertical" : secondUrls[choice2['choiceItem']]
                            }, context=getContext())
                            if insertProductJancodeSerializer.is_valid():
                                insertProductJancodeSerializer.save()
                            else:
                                return Response({"success" : False, "errors": insertProductJancodeSerializer.errors}, status=status.HTTP_200_OK)

            return Response({"success" : True}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success" : False, "error": str(e)}, status=status.HTTP_200_OK)


class UserUpdateBackground(APIView):
    parser_classes = [MultiPartParser]
    def post(self, request, userId, format='json'):
        return Response({"success" : True})

@csrf_exempt
def change_language(request):
    """
    API to change language.
    """

    language = request.POST.get('language', 'ja')
    request_url = request.POST.get('req_url', '')
    deactivate_all()
    activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language
    # request.LANGUAGE_CODE = translation.get_language()
    if request_url == '':
        response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        response = HttpResponseRedirect(request_url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response
