from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from products import views

urlpatterns = [
    url(r'^product_list/$', views.product_list, name='product_list'),
    url(r'^product_list_json/$', views.ProductList__asJson, name='ProductList__asJson'),
    url(r'^product_add/$', views.product_add, name='product_add'),
    url(r'^product_edit/(?P<product_id>.*)/$', views.product_edit, name='product_edit'),
    url(r'^product_delete/(?P<product_id>.*)/$', views.product_delete, name='product_delete'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
