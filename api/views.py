from django.contrib.auth.models import User, Group
from orders.models import Order, OrderProduct, OrderProductCommission, OrderReceipt, TotalSale, TotalCommission
from policies.models import Policy
from images.models import Image
from rest_framework import filters
from prefectures.models import Prefecture, CountryCode
from products.models import ProductCategory, Product, ProductImage, ProductVariety, ProductVarietySelection, ProductJancode
from profiles.models import FinancialAccount, Authority, Profile, UserSale, UserCommision, MonthlyPayment, Address
from taxes.models import TaxRate
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
import requests
import json
import stripe
import ast
from django.conf import settings
from datetime import date
import uuid

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
    queryset = Policy.objects.all()
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
        profiles = Profile.objects.filter(id__in=request.data['users'])
        profileSerializer = ProfileSerializer(profiles, many=True, context=getContext())
        images = []
        for profile in profileSerializer.data:
            if profile['image'] and profile['image']['image']:
                images.append(profile['image']['image'])
            else:
                images.append("")
        return Response({"success" : False, "images": images}, status=status.HTTP_200_OK)

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

                profileItem = {
                    'user' : userSerializer.data['url'],
                    'tel' : request.data['username'].replace("+" + request.data['callingCode'], ""),
                    'nickname' : request.data['nickname'],
                    'user_code' : user.id,
                    'authority' : authoritySerializer.data['url'],
                    'is_seller' : is_seller,
                    'tel_code': "+" + request.data['callingCode']
                }
                if request.data['introducer']:
                    introducerProfile = None
                    try:
                        introducerProfile = Profile.objects.get(id=int(request.data['introducer']))
                    except Exception as e:
                        print(e)
                    if introducerProfile:
                        introducerProfileSerializer = InsertProfileSerializer(introducerProfile, context=getContext())
                        profileItem['introducer'] = introducerProfileSerializer.data['url']
                else:
                    introducerProfile = None
                    try:
                        introducerProfile = Profile.objects.get(is_master=1)
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
                profile = Profile.objects.get(user_id=user.id)
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
            profile = Profile.objects.get(tel=request.data['tel_code'] + request.data['tel'])
        except Exception as e:
            print(e)

        if profile is None:
            try:
                profile = Profile.objects.get(tel = "+" + request.data['tel_code'] + request.data['tel'])
            except Exception as e:
                print(e)

        if profile is None:
            try:
                profile = Profile.objects.get(tel = request.data['tel'])
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
            profile = Profile.objects.get(tel=request.data['tel'])
        except Exception as e:
            print(e)

        if profile is None:
            try:
                profile = Profile.objects.get(tel = "+" + request.data['tel'])
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
            profile = Profile.objects.get(tel=request.data['tel'])
        except Exception as e:
            print(e)

        if profile is None:
            try:
                profile = Profile.objects.get(tel = "+" + request.data['tel'])
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
        orders = Order.objects.filter(purchaser=userId)
        orderSerializer = OrderSerializer(orders, many=True, context=getContext())
        updateOrders = []
        for order in orderSerializer.data:
            # order['seller'] = getObject(order['seller'])
            updateOrders.append(order)
        return Response({"success" : True, "orders" : updateOrders}, status=status.HTTP_200_OK)

class OrderProductList(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        orders = Order.objects.filter(purchaser=userId)
        orderProducts = OrderProduct.objects.filter(order__in=orders)
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
        orders = Order.objects.filter(seller=userId).values_list('id', flat=True)
        orderProducts = OrderProduct.objects.filter(order__in=orders)
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
        orders = Order.objects.filter(seller=userId).values_list('id', flat=True)
        orderProducts = OrderProduct.objects.filter(order__in=orders).values_list('id', flat=True)
        orderProductsCommission = OrderProductCommission.objects.filter(order_product__in=orderProducts)
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
        addresses = Address.objects.filter(user=userId)
        addressSerializer = AddressSerializer(addresses, many=True, context=getContext())
        updatedAddress = []
        for address in addressSerializer.data:
            # address['prefecture'] = getObject(address['prefecture'])
            updatedAddress.append(address)
        return Response({"success" : True, "addresses" : updatedAddress}, status=status.HTTP_200_OK)

class CustomerList(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        profiles = Profile.objects.filter(introducer_id=userId)
        profileSerializer = ProfileSerializer(profiles, many=True, context=getContext())
        return Response({"success" : True, "customers" : profileSerializer.data}, status=status.HTTP_200_OK)

class FinancialAccountGet(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        financialAccount = FinancialAccount.objects.filter(user=userId)
        if len(financialAccount) > 0:
            financialAccount = financialAccount[0]
        else:
            financialAccount = FinancialAccount()
        financialAccountSerialier = FinancialAccountSerialier(financialAccount, context=getContext())
        return Response({"success" : True, "financialAccount" : financialAccountSerialier.data}, status=status.HTTP_200_OK)

class ProductByIds(APIView):
    serializer_class = ProductSerializer

    def get(self, request, format='json'):
        products = Product.objects.filter(id__in=request.GET.getlist('ids[]'))
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
                    profile = Profile.objects.get(id=request.GET['userId'])
                    sProfileSerializer = ProfileSerializer(profile, context=getContext())

                    masters = Profile.objects.filter(is_master=1)
                    ids.extend(masters.values_list('id', flat=True))

                    if sProfileSerializer.data['authority']['id'] == 1:
                        profiles = Profile.objects.all()
                        ids.extend(Profile.objects.all().values_list('id', flat=True))
                    elif sProfileSerializer.data['introducer'] is not None:
                        introducers = sProfileSerializer.data['introducer'].split("/")
                        introducer = introducers[len(introducers)-2]
                        ids.append(introducer)
                        ids.extend(Profile.objects.filter(introducer_id=sProfileSerializer.data['id']).values_list('id', flat=True))


            profiles = Profile.objects.filter(id__in=ids)
            if len(profiles) == 0:
                return Response({"success" : True, "users" : profiles}, status=status.HTTP_200_OK)

            profileSerializer = ProfileSerializer(profiles, many=True, context=getContext())
            return Response({"success" : True, "users" : profileSerializer.data, "data" : request.GET}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"success" : False, "error": str(e)}, status=status.HTTP_200_OK)

def calculateCommission(price, orderProduct, userId, shipping_fee):
    profile = Profile.objects.get(id=userId)
    if profile:
        profileSerializer = ProfileSerializer(profile, context=getContext())
        if profileSerializer.data['introducer']:
            introducers = profileSerializer.data['introducer'].split("/")
            introducer = introducers[len(introducers)-2]
            introducer = Profile.objects.get(id=introducer)
            if introducer:
                introducerSerializer = ProfileSerializer(introducer, context=getContext())
                commission = introducerSerializer.data['authority']['official_commission_rate']
                if float(commission) > 0:
                    orderProductComm = {
                        'amount' : int(float(price) * float(commission)),
                        'is_sales' : 0,
                        'shipping_fee' : shipping_fee,
                        'order_product' : orderProduct,
                        'user' : introducerSerializer.data['url']
                    }
                    orderProductCommissionSerializer = InsertOrderProductCommissionSerializer(data=orderProductComm, context=getContext())

                    if orderProductCommissionSerializer.is_valid():
                        orderProductCommissionSerializer.save()
                    else:
                        return orderProductCommissionSerializer.errors

                    today_date = date.today()
                    year = today_date.year
                    month = today_date.month

                    totalComm = None
                    try:
                        totalComm = TotalCommission.objects.get(year=year, month=month, authority=profile.authority.id)
                        totalComm.order_count = totalComm.order_count + 1
                        totalComm.amount = totalComm.amount + int(float(price) * float(commission))
                        totalComm.save()
                    except Exception as e:
                        orderTotalComm = {
                            "year" : year,
                            "month" : month,
                            "order_count": 1,
                            "amount" : int(float(price) * float(commission)),
                            "authority" : introducerSerializer.data['authority']['url']
                        }
                        totalCommissionSerializer = TotalCommissionSerializer(data=orderTotalComm, context=getContext())
                        if totalCommissionSerializer.is_valid():
                            totalCommissionSerializer.save()
                        else:
                            return totalCommissionSerializer.errors

                    userCommission = None
                    try:
                        userCommission = UserCommision.objects.get(year=year, month=month, user_id=userId)
                        userCommission.order_count = userCommission.order_count + 1
                        userCommission.amount = userCommission.amount + int(float(price) * float(commission))
                        userCommission.tax = userCommission.tax + int(float(price) * float(commission))
                        userCommission.save()
                    except Exception as e:
                        userCommissionObj = {
                            "year": year,
                            "month" : month,
                            "order_count" : 1,
                            "amount" : int(float(price) * float(commission)),
                            "tax" : 0,
                            "total_amount" : int(float(price) * float(commission)),
                            "user" : introducerSerializer.data['url']
                        }
                        userCommissionSerializer = UserCommisionSerializer(data=userCommissionObj, context=getContext())
                        if userCommissionSerializer.is_valid():
                            userCommissionSerializer.save()
                        else:
                            return userCommissionSerializer.errors
                return calculateCommission(price, orderProduct, introducerSerializer.data['id'], shipping_fee)
    return

class ProductJanCodes(APIView):
    def get(self, request, productId, format='json'):
        productVarieties = ProductVariety.objects.filter(product_id=productId).values_list('id', flat=True)
        productVarietySelections = ProductVarietySelection.objects.filter(product_variety_id__in=productVarieties).values_list('id', flat=True)
        horizontal = ProductJancode.objects.filter(horizontal_id__in=productVarietySelections)
        vertical = ProductJancode.objects.filter(vertical_id__in=productVarietySelections)
        horizontalSerializer = ProductJancodeSerializer(horizontal, many=True, context=getContext())
        verticalSerializer = ProductJancodeSerializer(vertical, many=True, context=getContext())
        return Response({"success" : True, "verticals" : verticalSerializer.data, "horizontals" : horizontalSerializer.data}, status=status.HTTP_200_OK)

class RemoveReferral(APIView):
    def post(self, request, format='json'):
        user = request.data['userId']
        parent = request.data['parentId']
        profiles = Profile.objects.filter(id=user).filter(introducer_id=parent)
        profile = profiles[0]
        profile.introducer = None
        profile.save()
        return Response({"success" : True}, status=status.HTTP_200_OK)

class OrderReceipt(APIView):
    def post(self, request, orderId, format='json'):
        user = request.data['userId']
        parent = request.data['parentId']
        profiles = Profile.objects.filter(id=user).filter(introducer_id=parent)
        profile = profiles[0]
        profile.introducer = None
        profile.save()
        return Response({"success" : True}, status=status.HTTP_200_OK)

class Pay(APIView):
    def post(self, request, userId, format='json'):
        stripe.api_key = "sk_test_siDHJkaiXknooQGf1pStMNWY"
        try:
            if(len(request.data['products']) == 0):
                return Response({"success" : False, "errors": {"no_products" : "No products"}}, status=status.HTTP_200_OK)

            token = stripe.Token.create(
                card={
                    "number": request.data['card']['number'].replace(" ", ""),
                    "exp_month": request.data['card']['expiry'].split("/")[0],
                    "exp_year": "20" + request.data['card']['expiry'].split("/")[1],
                    "cvc": request.data['card']['cvc'],
                },
            )
            sellers = []
            profile = Profile.objects.get(id=userId)
            tax = TaxRate.objects.get(id=request.data['tax'])
            token_id = token.id
            customer_id = None

            ids = []
            quantities = {}
            varieties = {}

            for product in request.data['products']:
                quantities['item_' + str(product['product_id'])] = product['quantity']
                varieties['item_' + str(product['product_id'])] = product['varietyId']
                ids.append(product['product_id'])

            products = Product.objects.filter(id__in=ids)
            address = Address.objects.get(id=request.data['address'])

            groupProducts = {}
            orderIds = []

            if products and profile and address:
                profileSerializer = ProfileSerializer(profile, context=getContext())
                productSerializer = ProductSerializer(products, many=True, context=getContext())
                addressSerializer = AddressSerializer(address, context=getContext())

                total_amount = 0

                for product in productSerializer.data:
                    quantity = quantities['item_' + str(product['id'])]
                    if profileSerializer.data['is_seller']:
                        total_amount = float(total_amount) + (float(product['store_price']) * float(quantity))
                    else:
                        total_amount = float(total_amount) + (float(product['price']) * float(quantity))
                    total_amount = float(total_amount) + float(product['shipping_fee'])

                    if product['user']['url'] in groupProducts:
                        tmpProducts = groupProducts[product['user']['url']]
                        tmpProducts.append(product)
                        groupProducts[product['user']['url']] = tmpProducts
                    else:
                        groupProducts[product['user']['url']] = [product]

                charge = stripe.Charge.create(
                    amount=int(float(total_amount)),
                    currency="jpy",
                    source=token_id,
                    description="Order by " + str(profileSerializer.data['id']),
                )

                for product in productSerializer.data:
                    quantity = quantities['item_' + str(product['id'])]
                    price = 0
                    groupTotal = 0
                    groupShippingFee = float(product['shipping_fee'])

                    if profileSerializer.data['is_seller']:
                        price= float(product['store_price'])
                        groupTotal = (float(product['store_price']) * float(quantity))
                    else:
                        price= float(product['price'])
                        groupTotal = (float(product['price']) * float(quantity))
                    groupTax = int(float(groupTotal) * float(tax.tax_rate))

                    address2 = addressSerializer.data['address2']
                    if address2 is None:
                        address2 = "no_address_2"

                    order = {
                        'amount' : int(float(groupTotal)),
                        'tax': groupTax,
                        'shipping_fee': groupShippingFee,
                        # 'shipped_date': '',
                        'total_amount': int(float(groupTotal) + float(groupTax) + float(groupShippingFee)),
                        'name': addressSerializer.data['name'],
                        'zip1': addressSerializer.data['zip1'],
                        'tel_code': addressSerializer.data['tel_code'],
                        'address1': addressSerializer.data['address1'],
                        'address2': address2,
                        'tel': addressSerializer.data['tel'],
                        'is_hidden': 0,
                        'prefecture': addressSerializer.data['prefecture']['url'],
                        'seller': product['user']['url'],
                        'purchaser' : profileSerializer.data['url'],
                        'status' : 1
                    }
                    orderSerializer = InsertOrderSerializer(data=order, context=getContext())
                    if orderSerializer.is_valid():
                        newOrder = orderSerializer.save()
                        varietyId = varieties['item_' + str(product['id'])]

                        variety = None
                        variety = ProductJancode.objects.get(id=varietyId)
                        varietySerializer = ProductJancodeSerializer(variety, context=getContext())
                        variety = varietySerializer.data['url']

                        orderIds.append(orderSerializer.data['id'])

                        shop_name = ""
                        if product['user']['nickname']:
                            shop_name = product['user']['nickname']
                        if product['user']['real_name']:
                            shop_name = product['user']['real_name']
                        if product['user']['shop_name']:
                            shop_name = product['user']['shop_name']

                        orderReceipt = {
                            'is_copy' : 0,
                            'to_name' : addressSerializer.data['name'],
                            'amount' : groupTotal,
                            'output_date' : date.today(),
                            'order_date' : date.today(),
                            'product_name' : product['name'],
                            'shop_name' : shop_name,
                            'address' : addressSerializer.data['address1'],
                            'order' : orderSerializer.data['url'],
                            'payment' : charge['id']
                        }
                        orderReceiptSerializer = OrderReceiptSerializer(data=orderReceipt, context=getContext())
                        if orderReceiptSerializer.is_valid():
                            orderReceiptSerializer.save()
                        else:
                            return Response({"success" : False, "errors" : orderReceiptSerializer.errors}, status=status.HTTP_200_OK)

                        orderProduct = {
                            'quantity':  quantity,
                            'unit_price' : int(float(price)),
                            'total_price' : int(float(groupTotal)),
                            'tax': int(float(groupTax)),
                            'total_amount': int(float(groupTotal) + float(groupTax)),
                            'order': orderSerializer.data['url'],
                            'product_jan_code': variety
                        }
                        productJancode = ProductJancode.objects.get(id=varietyId)


                        today_date = date.today()
                        year = today_date.year
                        month = today_date.month

                        totalSale = None
                        userSale = None
                        monthlyPayment = None

                        # Total Sales
                        try:
                            totalSale = TotalSale.objects.get(year=year, month=month)
                            totalSale.sales_amount = totalSale.sales_amount + groupTotal
                            totalSale.tax = totalSale.tax + groupTax
                            totalSale.amount_tax_included = totalSale.amount_tax_included + groupTax + groupTotal
                            totalSale.shipping_fee = totalSale.shipping_fee + groupShippingFee
                            userSale.total_amount = userSale.total_amount + groupTax + groupTotal + groupShippingFee
                            totalSale.order_count = totalSale.order_count + 1
                            totalSale.save()
                        except Exception as e:
                            totalSaleObject = {
                                "year" : year,
                                "month" : month,
                                "sales_amount" : int(float(groupTotal)),
                                "tax" : int(float(groupTax)),
                                "amount_tax_included" : int(float(groupTax) + float(groupTotal)),
                                "shipping_fee" : int(float(groupShippingFee)),
                                "total_amount": int(float(groupTax) + float(groupTotal) + float(groupShippingFee)),
                                "order_count" : 1
                            }
                            totalSaleSerializer = TotalSaleSerializer(data=totalSaleObject, context=getContext())
                            if totalSaleSerializer.is_valid():
                                totalSaleSerializer.save()
                            else:
                                return Response({"success" : False, "errors" : totalSaleSerializer.errors}, status=status.HTTP_200_OK)

                        # # User Sale
                        try:
                            userSale = UserSale.objects.get(year=year, month=month, user_id=product['user']['id'])
                            userSale.order_count = userSale.order_count + 1
                            userSale.sales_amount = userSale.sales_amount + groupTotal
                            userSale.tax = userSale.tax + groupTax
                            userSale.amount_tax_included = userSale.amount_tax_included + groupTax + groupTotal
                            userSale.shipping_fee = userSale.shipping_fee + groupShippingFee
                            userSale.total_amount = userSale.total_amount + groupTax + groupTotal + groupShippingFee
                            userSale.save()
                        except Exception as e:
                            userSaleObject = {
                                "year" : year,
                                "month" : month,
                                "order_count" : 1,
                                "sales_amount" : groupTotal,
                                "tax" : groupTax,
                                "amount_tax_included" : groupTax + groupTotal,
                                "shipping_fee" : groupShippingFee,
                                "total_amount": int(float(groupTax) + float(groupTotal) + float(groupShippingFee)),
                                "user" : product['user']['url']
                            }
                            userSaleSerializer = UserSaleSerializer(data=userSaleObject, context=getContext())
                            if userSaleSerializer.is_valid():
                                userSaleSerializer.save()
                            else:
                                return Response({"success" : False, "errors" : userSaleSerializer.errors}, status=status.HTTP_200_OK)

                        # # Monthly Payment
                        try:
                            monthlyPayment = MonthlyPayment.objects.get(year=year, month=month, user_id=profileSerializer.data['id'])
                            monthlyPayment.amount = monthlyPayment.amount + groupTotal
                            monthlyPayment.save()
                        except Exception as e:
                            monthlyPaymentObject = {
                                "year" : year,
                                "month" : month,
                                "amount" : groupTotal,
                                "user" : profileSerializer.data['url']
                            }
                            monthlyPaymentSerializer = MonthlyPaymentSerializer(data=monthlyPaymentObject, context=getContext())
                            if monthlyPaymentSerializer.is_valid():
                                monthlyPaymentSerializer.save()
                            else:
                                return Response({"success" : False, "errors" : monthlyPaymentSerializer.errors}, status=status.HTTP_200_OK)

                        if productJancode:
                            productJancode.stock = int(productJancode.stock) - int(quantity)
                            productJancode.save()

                        orderProductSerializer = InsertOrderProductSerializer(data=orderProduct, context=getContext())

                        orderProductComm = {
                            'amount' : groupTotal,
                            'is_sales' : 1,
                            'shipping_fee' : groupShippingFee,
                            'order_product' : orderProductSerializer.data['url'],
                            'user' : product['user']['url']
                        }
                        orderProductCommissionSerializer = InsertOrderProductCommissionSerializer(data=orderProductComm, context=getContext())
                        if orderProductCommissionSerializer.is_valid():
                            orderProductCommissionSerializer.save()
                        else:
                            return Response({"success" : False, "errors" : orderProductCommissionSerializer.errors}, status=status.HTTP_200_OK)

                        if orderProductSerializer.is_valid():
                            orderProductSerializer.save()
                            errors = calculateCommission(price, orderProductSerializer.data['url'], profileSerializer.data['id'], product['shipping_fee'])
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
            return Response({"success" : False, "error": str(e)}, status=status.HTTP_200_OK)

class UpdateProfileImage(APIView):
    def post(self, request, userId, format='json'):
        profile = Profile.objects.get(id=userId)
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
                noneVariationItems = request.data['noneVariationItems']
                if noneVariationItems['janCode'] == "" and 'delete' in noneVariationItems and not noneVariationItems['delete']:
                    return Response({"success" : False, "errors" : ["Please fill in Jan Code."]}, status=status.HTTP_200_OK)
                if noneVariationItems['stock'] == "" and 'delete' in noneVariationItems and not noneVariationItems['delete']:
                    return Response({"success" : False, "errors" : ["Please fill in stock."]}, status=status.HTTP_200_OK)
                variety = 0
            if request.data['productVariation'] == 'one':
                oneVariationItems = request.data['oneVariationItems']
                for item in oneVariationItems['items']:
                    if item['janCode'] == "" and 'delete' in item and not item['delete']:
                        return Response({"success" : False, "errors" : ["Please fill in Jan Code."]}, status=status.HTTP_200_OK)
                    if item['stock'] == "" and 'delete' in item and not item['delete']:
                        return Response({"success" : False, "errors" : ["Please fill in stock."]}, status=status.HTTP_200_OK)
                variety = 1
            if request.data['productVariation'] == 'two':
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

            profile = Profile.objects.get(id=userId)
            profileSerializer = ProfileSerializer(profile, context=getContext())

            productData = {
                "name" : request.data['productName'],
                "brand_name" : request.data["brandName"],
                "pr" : request.data["pr"],
                "url_str" : request.data['productId'],
                "variety" : variety,
                "opened_date" : request.data['publishDate'],
                "price" : request.data['price'],
                "store_price" : request.data['storePrice'],
                "shipping_fee": request.data['shipping'],
                "description" : request.data['productDescription'],
                "category" : request.data['productCategory'],
                "user" : profileSerializer.data['url']
            }
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
        product = Product.objects.get(id=request.GET['productId'])
        productSerializer = ProductSerializer(product, context=getContext())
        janCodes = []
        for productVariety in productSerializer.data['productVarieties']:
            for productVarietySelection in productVariety['productVarietySelections']:
                for horizontal in productVarietySelection['jancode_horizontal']:
                    janCodes.append(horizontal['jan_code'])
                for vertical in productVarietySelection['jancode_vertical']:
                    janCodes.append(vertical['jan_code'])
        productJancodes = ProductJancode.objects.filter(jan_code__in=janCodes)
        productJancodesSerializer = ProductJancodeSerializer(productJancodes, many=True, context=getContext())


        horizontals = ProductJancode.objects.filter(jan_code__in=janCodes).values_list('horizontal_id', flat=True)
        verticals = ProductJancode.objects.filter(jan_code__in=janCodes).values_list('vertical_id', flat=True)
        janCodeIds = []
        janCodeIds.extend(horizontals)
        janCodeIds.extend(verticals)
        productVarietyIDs = ProductVarietySelection.objects.filter(id__in=janCodeIds).values_list("product_variety_id", flat=True)
        productIDs = ProductVariety.objects.filter(id__in=productVarietyIDs).values_list("product_id", flat=True)
        products = Product.objects.filter(id__in=productIDs)
        productSerializer = SimpleProductSerializer(products, many=True, context=getContext())
        return Response({"success" : True, "products" : productSerializer.data}, status=status.HTTP_200_OK)


class EditProduct(APIView):
    def post(self, request, userId, format='json'):
        try:
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
                noneVariationItems = request.data['noneVariationItems']
                if noneVariationItems['janCode'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in Jan Code."]}, status=status.HTTP_200_OK)
                if noneVariationItems['stock'] == "":
                    return Response({"success" : False, "errors" : ["Please fill in stock."]}, status=status.HTTP_200_OK)
                variety = 0
            if request.data['productVariation'] == 'one':
                oneVariationItems = request.data['oneVariationItems']
                for item in oneVariationItems['items']:
                    if item['janCode'] == "":
                        return Response({"success" : False, "errors" : ["Please fill in Jan Code."]}, status=status.HTTP_200_OK)
                    if item['stock'] == "":
                        return Response({"success" : False, "errors" : ["Please fill in stock."]}, status=status.HTTP_200_OK)
                variety = 1
            if request.data['productVariation'] == 'two':
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

            profile = Profile.objects.get(id=userId)
            profileSerializer = ProfileSerializer(profile, context=getContext())


            product = Product.objects.get(id=request.data['id'])
            product.name = request.data['productName']
            product.brand_name = request.data["brandName"]
            product.pr = request.data["pr"]
            product.url_str = request.data["productId"]
            product.variety = variety
            product.opened_date = request.data["publishDate"]
            product.price = request.data["price"]
            product.store_price = request.data["storePrice"]
            product.shipping_fee = request.data["shipping"]
            product.description = request.data["productDescription"]

            productCategories = request.data['productCategory'].split("/")
            productCategoryId = productCategories[len(productCategories)-2]
            productCategory = ProductCategory.objects.get(id=productCategoryId)

            product.category = productCategory
            if request.data['publishState'] == 'published':
                product.is_opened = 1
            else:
                product.is_opened = 0

            if request.data['productStatus'] == 'new':
                product.is_used = 0
            else:
                product.is_used = 1

            if request.data['draft']:
                product.is_draft = 1
            else:
                product.is_draft = 0

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
