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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import include, path
from profiles import views
from api import views as api_views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'api/users', api_views.UserViewSet)
router.register(r'api/groups', api_views.GroupViewSet)
router.register(r'api/orders', api_views.OrderViewSet)
router.register(r'api/order_products', api_views.OrderProductViewSet)
router.register(r'api/order_product_commission', api_views.OrderProductCommissionViewSet)
router.register(r'api/order_receipts', api_views.OrderReceiptViewSet)
router.register(r'api/total_sales', api_views.TotalSaleViewSet)
router.register(r'api/total_commissions', api_views.TotalCommissionViewSet)
router.register(r'api/policies', api_views.PolicyViewSet)
router.register(r'api/prefectures', api_views.PrefectureViewSet)
router.register(r'api/product_categories', api_views.ProductCategoryViewSet)
router.register(r'api/products', api_views.ProductViewSet)
router.register(r'api/product_images', api_views.ProductImageViewSet)
router.register(r'api/product_varieties', api_views.ProductVarietyViewSet)
router.register(r'api/product_variety_selections', api_views.ProductVarietySelectionViewSet)
router.register(r'api/product_jancodes', api_views.ProductJancodeViewSet)
router.register(r'api/authorities', api_views.AuthorityViewSet)
router.register(r'api/profiles', api_views.ProfileViewSet)
router.register(r'api/user_sales', api_views.UserSaleViewSet)
router.register(r'api/user_commissions', api_views.UserCommisionViewSet)
router.register(r'api/monthly_payments', api_views.MonthlyPaymentViewSet)
router.register(r'api/addresses', api_views.AddressViewSet)
router.register(r'api/tax_rates', api_views.TaxRateViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^orders/', include('orders.urls')),
    # url(r'^images/', include('images.urls')),
    # url(r'^policies/', include('policies.urls')),
    # url(r'^prefectures/', include('prefectures.urls')),
    # url(r'^products/', include('products.urls')),
    url(r'^profiles/', include('profiles.urls')),
    # url(r'^salons/', include('salons.urls')),
    # url(r'^taxes/', include('taxes.urls')),
    url(r'^$', views.home_load, name='home_load'),
    url(r'^pass_reset/$', views.pass_reset, name='pass_reset'),
    url(r'^reset_password/$', views.reset_password, name='reset_password'),
    url(r'^master_login/$', views.login_master, name='login_master'),
    url(r'^sales_login/$', views.login_sales, name='login_sales'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
]
urlpatterns += router.urls