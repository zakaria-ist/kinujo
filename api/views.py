from django.contrib.auth.models import User, Group
from orders.models import Order, OrderProduct, OrderProductCommission, OrderReceipt, TotalSale, TotalCommission
from policies.models import Policy
from prefectures.models import Prefecture
from products.models import ProductCategory, Product, ProductImage, ProductVariety, ProductVarietySelection, ProductJancode
from profiles.models import Authority, Profile, UserSale, UserCommision, MonthlyPayment, Address
from taxes.models import TaxRate
from rest_framework import viewsets, status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import activate, deactivate_all
from .serializers import UserSerializer, GroupSerializer,  OrderSerializer, OrderProductSerializer, OrderProductCommissionSerializer, OrderReceiptSerializer, TotalSaleSerializer, TotalCommissionSerializer, PolicySerializer, PrefectureSerializer, ProductCategorySerializer, ProductSerializer, ProductImageSerializer, ProductVarietySerializer, ProductVarietySelectionSerializer, ProductJancodeSerializer, AuthoritySerializer, ProfileSerializer, UserSaleSerializer, UserCommisionSerializer, MonthlyPaymentSerializer, AddressSerializer, TaxRateSerializer
from rest_framework.test import APIRequestFactory
import requests 
import json

def getContext():
    factory = APIRequestFactory()
    n = factory.get('/')
    context = {
        'request': Request(APIRequestFactory().get('/')),
    }
    return context

def getObject(url):
    url = url.replace("testserver", "127.0.0.1:8000")
    return requests.get(url = url).json()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


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
    serializer_class = ProfileSerializer

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
        userSerializer = UserSerializer(data=request.data, context=getContext())
        if userSerializer.is_valid():
            user = userSerializer.save()

            authority = Authority.objects.get(id=1)
            is_seller = 0
            if request.data['authority'] == 'store':
                authority = Authority.objects.get(id=2)
                is_seller = 1
                
            authoritySerializer = AuthoritySerializer(authority, context=getContext())
        
            profileSerializer = ProfileSerializer(data={
                'user' : userSerializer.data['url'],
                'tel' : request.data['username'],
                'password' : request.data['password'],
                'nickname' : request.data['nickname'],
                'user_code' : user.id,
                'authority' : authoritySerializer.data['url'],
                'is_seller' : is_seller
            }, context=getContext())
            if profileSerializer.is_valid():
                profile = profileSerializer.save()
                if user:
                    data = profileSerializer.data
                    data['authority'] = getObject(data['authority'])
                    data['user'] = getObject(data['user'])
                    return Response({"success": True, "data" : {
                        "user" : data
                    }}, status=status.HTTP_201_CREATED)
            else:
                print(profileSerializer.errors)
                return Response({"success" : False, "errors" : profileSerializer.errors}, status=status.HTTP_200_OK)
        else:
            print(userSerializer.errors)
            return Response({"success" : False, "errors": userSerializer.errors}, status=status.HTTP_200_OK)
     
class CheckRegister(APIView):
    def post(self, request, format='json'):
        userSerializer = UserSerializer(data=request.data, context=getContext())
        if userSerializer.is_valid():
            return Response({"success" : True}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "error" : "invalid"}, status=status.HTTP_200_OK)

class UserLogin(APIView):
    def post(self, request, format='json'):
        profile = Profile.objects.get(tel=request.data['tel'])
        if profile:
            user = User.objects.get(id = profile.user_id)
            if user:
                if user.check_password(request.data['password']):
                    profileSerializer = ProfileSerializer(profile, context=getContext())
                    data = profileSerializer.data
                    data['authority'] = getObject(data['authority'])
                    data['user'] = getObject(data['user'])
                    return Response({"success" : True, "data" : {
                        "user" : data
                    }}, status=status.HTTP_200_OK)
                else:
                    return Response({"success" : False, "error" : "incorrect_password"}, status=status.HTTP_200_OK)
            else:
                return Response({"success" : False, "error" : "account_not_exists"}, status=status.HTTP_200_OK)
        else:
            return Response({"success" : False, "error" : "account_not_exists"}, status=status.HTTP_200_OK)

class PasswordReset(APIView):
    def post(self, request, format='json'):
        profile = Profile.objects.get(tel=request.data['tel'])
        if profile:
            user = User.objects.get(id = profile.user_id)
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
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
