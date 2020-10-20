from django.conf.urls import url
from . import views
from rest_framework import routers

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
    url(r'user/register/check', views.CheckRegister.as_view(), name='check-register'),
    url(r'user/register', views.UserRegister.as_view(), name='user-register'),
    url(r'password/reset', views.PasswordReset.as_view(), name='password-reset'),
    url(r'user/login', views.UserLogin.as_view(), name='user-login'),
    url(r'app/config', views.AppConfig.as_view(), name='app-config'),
    url('^products/(?P<userId>.+)/$', views.ProductList.as_view()),
    url('^customers/(?P<userId>.+)/$', views.CustomerList.as_view()),
    url(r'^change-language/$', views.change_language, name='change_language'),
]
urlpatterns += router.urls