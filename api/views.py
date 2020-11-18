from django.contrib.auth.models import User, Group
from orders.models import Order, OrderProduct, OrderProductCommission, OrderReceipt, TotalSale, TotalCommission
from policies.models import Policy
from images.models import Image
from rest_framework import filters
from prefectures.models import Prefecture
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
from .serializers import ImageSerializer, FinancialAccountSerialier, UserSerializer, GroupSerializer,  OrderSerializer, OrderProductSerializer, OrderProductCommissionSerializer, OrderReceiptSerializer, TotalSaleSerializer, TotalCommissionSerializer, PolicySerializer, PrefectureSerializer, ProductCategorySerializer, ProductSerializer, ProductImageSerializer, ProductVarietySerializer, ProductVarietySelectionSerializer, ProductJancodeSerializer, AuthoritySerializer, ProfileSerializer, UserSaleSerializer, UserCommisionSerializer, MonthlyPaymentSerializer, AddressSerializer, TaxRateSerializer
from rest_framework.test import APIRequestFactory
from rest_framework.parsers import MultiPartParser
import requests 
import json
import stripe
import ast
from django.conf import settings

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
    search_fields = ['nickname']
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

class TaxRateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = TaxRate.objects.all()
    serializer_class = TaxRateSerializer

class UserRegister(APIView):
    def post(self, request, format='json'):
        try:
            userSerializer = UserSerializer(data=request.data, context=getContext())
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
                    'tel' : request.data['username'],
                    'password' : request.data['password'],
                    'nickname' : request.data['nickname'],
                    'user_code' : user.id,
                    'authority' : authoritySerializer.data['url'],
                    'is_seller' : is_seller
                }
                if request.data['introducer']:
                    introducerProfile = None
                    try:
                        introducerProfile = Profile.objects.get(id=int(request.data['introducer']))
                    except Exception as e:
                        print(e)
                    if introducerProfile:
                        introducerProfileSerializer = ProfileSerializer(introducerProfile, context=getContext())
                        profileItem['introducer'] = introducerProfileSerializer.data['url']

                profileSerializer = ProfileSerializer(data=profileItem, context=getContext())
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
            return Response({"success" : True}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "errors" : userSerializer.errors}, status=status.HTTP_200_OK)

class UserLogin(APIView):
    def post(self, request, format='json'):
        profile = None
        try:
            profile = Profile.objects.get(tel=request.data['tel'])
        except Exception as e:
            print(e)
        if profile:
            user = None
            try:
                user = User.objects.get(id = profile.user_id)
            except Exception as e:
                print(e)
            if user:
                if user.check_password(request.data['password']):
                    profileSerializer = ProfileSerializer(profile, context=getContext())
                    data = profileSerializer.data
                    # data['authority'] = getObject(data['authority'])
                    # data['user'] = getObject(data['user'])
                    return Response({"success" : True, "data" : {
                        "user" : data
                    }}, status=status.HTTP_200_OK)
                else:
                    return Response({"success" : False, "error" : "Incorrect Password"}, status=status.HTTP_200_OK)
            else:
                return Response({"success" : False, "error" : "Account Not Exists"}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "error" : "Account Not Exists"}, status=status.HTTP_200_OK)

class PasswordReset(APIView):
    def post(self, request, format='json'):
        profile = None
        try:
            profile = Profile.objects.get(tel=request.data['tel'])
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

                    profile.password = request.data['password']
                    profile.save()
                    return Response({"success" : True}, status=status.HTTP_200_OK)
                else:
                    return Response({"success" : False, "error" : "password_mismatch"}, status=status.HTTP_200_OK)
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
        products = Product.objects.filter(user=userId);
        productSerializer = ProductSerializer(products, many=True, context=getContext())
        return Response({"success" : True, "products" : productSerializer.data}, status=status.HTTP_200_OK)

class OrderList(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        orders = Order.objects.filter(purchaser=userId);
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
        addresses = Address.objects.filter(user=userId);
        addressSerializer = AddressSerializer(addresses, many=True, context=getContext())
        updatedAddress = []
        for address in addressSerializer.data:
            # address['prefecture'] = getObject(address['prefecture'])
            updatedAddress.append(address)
        return Response({"success" : True, "addresses" : updatedAddress}, status=status.HTTP_200_OK)

class CustomerList(APIView):
    serializer_class = ProductSerializer

    def get(self, request, userId, format='json'):
        orders = Order.objects.filter(seller=userId).values_list('id', flat=True)
        profiles = Profile.objects.filter(id__in=orders)
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
        profiles = Profile.objects.filter(id__in=request.GET.getlist('ids[]'))
        profileSerializer = ProfileSerializer(profiles, many=True, context=getContext())
        return Response({"success" : True, "users" : profileSerializer.data}, status=status.HTTP_200_OK)

class Pay(APIView):
    def post(self, request, userId, format='json'):
        stripe.api_key = "sk_test_siDHJkaiXknooQGf1pStMNWY"
        try:
            token = stripe.Token.create(
                card={
                    "number": request.data['card']['number'].replace(" ", ""),
                    "exp_month": request.data['card']['expiry'].split("/")[0],
                    "exp_year": "20" + request.data['card']['expiry'].split("/")[1],
                    "cvc": request.data['card']['cvc'],
                },
            )

            profile = Profile.objects.get(id=userId)
            token_id = token.id
            customer_id = None

            if profile:
                profileSerializer = ProfileSerializer(profile, context=getContext())
                payload = profileSerializer.data['payload']
                payload = payload.replace("'", '"')
                if payload and payload is not None:
                    payload = payload.replace("'", '"')
                    payload = ast.literal_eval(payload)

                if  payload and payload is not None and 'customerId' in payload:
                    customer_id = payload["customerId"]
                else:
                    customer = stripe.Customer.create(
                        description=profileSerializer.data['id'],
                    )
                    customer_id = customer.id

                    payload["customerId"] = customer_id
                    profile.payload = json.dumps(payload)
                    profile.save()
            return Response({"success" : True, "params" : payload})
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

    language = request.POST['language']
    deactivate_all()
    activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language
    # request.LANGUAGE_CODE = translation.get_language()
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response
