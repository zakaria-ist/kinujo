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
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
