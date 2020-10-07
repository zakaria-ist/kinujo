from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.template import RequestContext
from django.contrib import messages

# Create your views here.
def creae_product(request):
    return render(request, 'create-product.html')