from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from profiles import views

urlpatterns = [
    url(r'^profile_list/$', views.profile_list, name='profile_list'),
    url(r'^profile_list_json/$', views.ProfileList__asJson, name='ProfileList__asJson'),
    url(r'^profile_add/$', views.profile_add, name='profile_add'),
    url(r'^profile_edit/(?P<profile_id>.*)/$', views.profile_edit, name='profile_edit'),
    url(r'^profile_delete/(?P<profile_id>.*)/$', views.profile_delete, name='profile_delete'),
    url(r'^get_financial_info/$', views.get_financial_info, name='get_financial_info'),
    url(r'^update_financial_info/$', views.update_financial_info, name='update_financial_info'),
    url(r'^get_shipping_info/$', views.get_shipping_info, name='get_shipping_info'),
    url(r'^update_shipping_info/$', views.update_shipping_info, name='update_shipping_info'),
    url(r'^delete_shipping_info/$', views.delete_shipping_info, name='delete_shipping_info'),
    url(r'^shipping_list_json/$', views.ShippingList__asJson, name='ShippingList__asJson'),
    url(r'^validate_user_phone/(?P<profile_id>.*)/$', views.validate_user_phone, name='validate_user_phone'),
    # url(r'^upload_profile_image/$', views.upload_profile_image, name='upload_profile_image'),

    # for sales section
    url(r'^sales_list/$', views.sales_list, name='sales_list'),
    url(r'^payment_list/$', views.payment_list, name='payment_list'),

    # for dynamic template rendering
    url(r'^templates/salon_form/$', views.salon_form, name='salon_form'),
    url(r'^templates/salon_table/$', views.salon_table, name='salon_table'),
    url(r'^templates/shipping_form/$', views.shipping_form, name='shipping_form'),
    url(r'^templates/shipping_table/$', views.shipping_table, name='shipping_table'),


    # for listing user
    url(r'^listing_sales_list/$', views.listing_sales_list, name='listing_sales_list'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
