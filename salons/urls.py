from django.conf.urls import url
from salons import views

urlpatterns = [
    url(r'^get_salon_info/$', views.get_salon_info, name='get_salon_info'),
    url(r'^update_salon_info/$', views.update_salon_info, name='update_salon_info'),
    url(r'^delete_salon_info/$', views.delete_salon_info, name='delete_salon_info'),
    url(r'^salon_list_json/$', views.SalonList__asJson, name='SalonList__asJson'),
]
