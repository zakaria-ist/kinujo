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
router.register(r'country_codes', views.CountryCodeViewSet)
router.register(r'product_categories', views.ProductCategoryViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'simple_products', views.SimpleProductViewSet)
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
router.register(r'insertAddresses', views.InsertAddressViewSet)
router.register(r'tax_rates', views.TaxRateViewSet)
router.register(r'financial_account', views.FinancialAccountViewSet)
router.register(r'images', views.ImageViewSet)

urlpatterns = [
    url('^user/background/(?P<userId>.+)/$', views.UserUpdateBackground.as_view()),
    url(r'user/register/check', views.CheckRegister.as_view(), name='check-register'),
    url(r'user/register', views.UserRegister.as_view(), name='user-register'),
    url(r'user/images', views.UserImages.as_view(), name='user-images'),
    url(r'user/alluser/data', views.AllUserImages.as_view(), name='alluser-images'),
    url(r'user/change-email', views.ChangeEmail.as_view(), name='user-change-email'),
    url(r'user/get-email', views.GetEmail.as_view(), name='user-get-email'),
    url(r'user/send-email', views.SendEmail.as_view(), name='user-send-email'),
    url(r'user/change-phone', views.ChangePhone.as_view(), name='user-cahnge-phone'),
    url(r'user/check-phone', views.CheckPhone.as_view(), name='user-check-phone'),
    url(r'password/reset', views.PasswordReset.as_view(), name='password-reset'),
    url(r'user/login', views.UserLogin.as_view(), name='user-login'),
    url(r'product/byIds', views.ProductByIds.as_view(), name='product-by-ids'),
    url(r'user/byIds', views.UserByIds.as_view(), name='user-by-ids'),
    url(r'app/config', views.AppConfig.as_view(), name='app-config'),
    url(r'removeReferral', views.RemoveReferral.as_view(), name='app-config'),
    url(r'getProductByVariety', views.GetProductByVariety.as_view(), name='app-config'),
    url('^createProduct/(?P<userId>.+)/$', views.CreateProduct.as_view()),
    url('^editProduct/(?P<userId>.+)/$', views.EditProduct.as_view()),
    url('^latestOrderReceipt/(?P<orderId>.+)/$', views.OrderReceipt.as_view()),
    url('^updateProfileImage/(?P<userId>.+)/$', views.UpdateProfileImage.as_view()),
    url('^sellerProducts/(?P<userId>.+)/$', views.ProductList.as_view()),
    url('^productJancodes/(?P<productId>.+)/$', views.ProductJanCodes.as_view()),
    url('^userOrders/(?P<userId>.+)/$', views.OrderList.as_view()),
    url('^customers/(?P<userId>.+)/$', views.CustomerList.as_view()),
    url('^addressList/(?P<userId>.+)/$', views.AddressList.as_view()),
    url('^orderProducts/(?P<userId>.+)/$', views.OrderProductList.as_view()),
    url('^saleProducts/(?P<userId>.+)/$', views.SaleProductList.as_view()),
    url('^commissionProducts/(?P<userId>.+)/$', views.CommissionProductList.as_view()),
    url('^financial-account/(?P<userId>.+)/$', views.FinancialAccountGet.as_view()),
    url('^pay/(?P<userId>.+)/$', views.Pay.as_view()),
    url(r'^change-language/$', views.change_language, name='change_language'),
]
urlpatterns += router.urls