"""kinujo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from profiles import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(r'^orders/', include('orders.urls')),
    # url(r'^images/', include('images.urls')),
    # url(r'^policies/', include('policies.urls')),
    # url(r'^prefectures/', include('prefectures.urls')),
    # url(r'^products/', include('products.urls')),
    # url(r'^profiles/', include('profiles.urls')),
    # url(r'^salons/', include('salons.urls')),
    # url(r'^taxes/', include('taxes.urls')),
    url(r'^$', views.home_load, name='home_load'),
    url(r'^pass_reset/$', views.pass_reset, name='pass_reset'),
    url(r'^reset_password/$', views.reset_password, name='reset_password'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^logout/$', views.logout_user, name='logout_user')
]
