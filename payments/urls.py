from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from payments import views

urlpatterns = [
    url(r'^pay/$', views.PayView.as_view(), name='pay'),
    # url(r'^success$', views.SuccessView.as_view(), name='success'),
    # url(r'^cancelled$', views.CancelledView.as_view(), name='cancelled'),
    url(r'^create-checkout-session/$', views.create_checkout_session, name='create_checkout_session'),
    url(r'^webhook/$', views.stripe_webhook, name='stripe_webhook'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
