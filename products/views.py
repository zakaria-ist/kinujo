from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.template import RequestContext
from django.contrib import messages

# Create your views here.
def item_registration(request):
    return render(request, 'item-registration.html')