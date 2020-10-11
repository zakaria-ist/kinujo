from django.contrib.auth.models import User, Group
from orders.models import Order, OrderProduct, OrderProductCommission, OrderReceipt, TotalSale, TotalCommission
from policies.models import Policy
from prefectures.models import Prefecture
from products.models import ProductCategory, Product, ProductImage, ProductVariety, ProductVarietySelection, ProductJancode
from profiles.models import Authority, Profile, UserSale, UserCommision, MonthlyPayment, Address
from taxes.models import TaxRate
from rest_framework import viewsets
from django.http import HttpResponseRedirect
from django.utils import translation
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import activate, deactivate_all
from .serializers import UserSerializer, GroupSerializer,  OrderSerializer, OrderProductSerializer, OrderProductCommissionSerializer, OrderReceiptSerializer, TotalSaleSerializer, TotalCommissionSerializer, PolicySerializer, PrefectureSerializer, ProductCategorySerializer, ProductSerializer, ProductImageSerializer, ProductVarietySerializer, ProductVarietySelectionSerializer, ProductJancodeSerializer, AuthoritySerializer, ProfileSerializer, UserSaleSerializer, UserCommisionSerializer, MonthlyPaymentSerializer, AddressSerializer, TaxRateSerializer


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

@csrf_exempt
def change_language(request):
    """
    API to change language.
    """

    language = request.POST['language']
    deactivate_all()
    activate(language)
    request.session[translation.LANGUAGE_SESSION_KEY] = language
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))