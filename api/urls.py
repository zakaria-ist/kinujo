from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^change-language/$', views.change_language, name='change_language'),
]
