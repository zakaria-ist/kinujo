from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from orders import views

urlpatterns = [
    url(r'^order_list/$', views.order_list, name='order_list'),
    url(r'^order_list_json/$', views.OrderList__asJson, name='OrderList__asJson'),
    url(r'^order_add/$', views.order_add, name='order_add'),
    url(r'^order_edit/(?P<order_id>.*)/$', views.order_edit, name='order_edit'),
    url(r'^order_delete/(?P<order_id>.*)/$', views.order_delete, name='order_delete'),
    url(r'^check_for_duplicate/(?P<type>.*)/(?P<value>.*)/$', views.check_for_duplicate, name='order_check_for_duplicate'),
    url(r'^export_order_list_as_csv/$', views.export_order_list_as_csv, name='export_order_list_as_csv'),

    # for commission & sales data
    url(r'^sales_list_json/$', views.UserSalesList__asJson, name='UserSalesList__asJson'),
    url(r'^commission_list_json/$', views.UserCommissionList__asJson, name='UserCommissionList__asJson'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
