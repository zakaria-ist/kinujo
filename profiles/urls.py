from django.conf.urls import url
from profiles import views

urlpatterns = [
    url(r'^profile_list/$', views.profile_list, name='profile_list'),
    url(r'^profile_list_json/(?P<auth_type>.*)/$', views.ProfileList__asJson, name='ProfileList__asJson'),
    url(r'^profile_add/$', views.profile_add, name='profile_add'),
    url(r'^profile_edit/(?P<profile_id>.*)/$', views.profile_edit, name='profile_edit'),
    url(r'^profile_delete/(?P<profile_id>.*)/$', views.profile_delete, name='profile_delete'),
    url(r'^upload_profile_image/$', views.upload_profile_image, name='upload_profile_image'),
]
