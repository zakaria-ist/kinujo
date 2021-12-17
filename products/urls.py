from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from products import views

urlpatterns = [
    url(r'^product_list/$', views.product_list, name='product_list'),
    url(r'^product_list_json/$', views.ProductList__asJson, name='ProductList__asJson'),
    url(r'^seller_product_list_json/$', views.SellerProductList__asJson, name='SellerProductList__asJson'),
    url(r'^small_product_list_json/$', views.smallProductList__asJson, name='smallProductList__asJson'),
    url(r'^recommended_product_list_json/$', views.recommendedProduct__asJson, name='recommendedProduct__asJson'),
    url(r'^product_add/$', views.product_add, name='product_add'),
    url(r'^product_edit/(?P<product_id>.*)/$', views.product_edit, name='product_edit'),
    url(r'^product_delete/(?P<product_id>.*)/$', views.product_delete, name='product_delete'),
    url(r'^add_update_product/$', views.add_update_product, name='add_update_product'),
    url(r'^get_product_info/$', views.get_product_info, name='get_product_info'),
    url(r'^delete_product/$', views.delete_product, name='delete_product'),
    url(r'^update_product_from_list/$', views.update_product_from_list, name='update_product_from_list'),
    url(r'^check_for_duplicate/(?P<type>.*)/(?P<value>.*)/$', views.check_for_duplicate, name='product_check_for_duplicate'),
    url(r'^update_varieties/$', views.update_varieties, name='update_varieties'),
    url(r'^export_product_list_as_csv/$', views.export_product_list_as_csv, name='export_product_list_as_csv'),
    url(r'^recommended_list/$', views.recommended_product_list, name='recommended_product_list'),
    url(r'^remove_recommended/$', views.remove_recommended_product, name='remove_recommended_product'),
    url(r'^sort_product/$', views.sort_product, name='sort_product'),
    url(r'^add_recommended/$', views.add_recommended, name='add_recommended'),    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
