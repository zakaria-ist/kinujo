from django.shortcuts import render
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# @login_required
def home_load(request):
    return render(request, 'base.html')

def pass_reset(request):
    return render(request, 'password-reset.html')

def reset_password(request):
    return render(request, 'login.html')

def login_user(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponsePermanentRedirect(reverse('home_load'))
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    return render(request, 'login.html')