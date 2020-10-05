"""kinujo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'orders', views.OrderViewSet)
router.register(r'order_products', views.OrderProductViewSet)
router.register(r'order_product_commission', views.OrderProductCommissionViewSet)
router.register(r'order_receipts', views.OrderReceiptViewSet)
router.register(r'total_sales', views.TotalSaleViewSet)
router.register(r'total_commissions', views.TotalCommissionViewSet)
router.register(r'policies', views.PolicyViewSet)
router.register(r'prefectures', views.PrefectureViewSet)
router.register(r'product_categories', views.ProductCategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'product_images', views.ProductImageViewSet)
router.register(r'product_varieties', views.ProductVarietyViewSet)
router.register(r'product_variety_selections', views.ProductVarietySelectionViewSet)
router.register(r'product_jancodes', views.ProductJancodeViewSet)
router.register(r'authorities', views.AuthorityViewSet)
router.register(r'profiles', views.ProfileViewSet)
router.register(r'user_sales', views.UserSaleViewSet)
router.register(r'user_commissions', views.UserCommisionViewSet)
router.register(r'monthly_payments', views.MonthlyPaymentViewSet)
router.register(r'addresses', views.AddressViewSet)
router.register(r'tax_rates', views.TaxRateViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
]