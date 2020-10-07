from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.urls import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ProfileForm, ImageUploadForm
from .models import Profile
from images.models import Image
from django.conf import settings as s
import datetime
import json
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

# @login_required
def profile_list(request):
    return render(request, 'profile_list.html')

@login_required
def ProfileList__asJson(request, order_type):
    draw = request.GET['draw']
    start = request.GET['start']
    length = request.GET['length']
    search = request.GET['search[value]']
    

    # content = {"draw": draw, "data": array, "recordsTotal": records_total, "recordsFiltered": records_filtered}
    # json_content = json.dumps(content, ensure_ascii=False)
    # return HttpResponse(json_content, content_type='application/json')

# @login_required
def upload_profile_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            m = form.save(commit=False)
            m.image = form.cleaned_data.get('profile_image')
            m.save()
            json_content = json.dumps({'image': m}, ensure_ascii=False)
            return HttpResponse(json_content, content_type='application/json')

# @login_required
def profile_add(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid:
            user = User.objects.create_user(request.POST.get('tel'), 'test@test.com', request.POST.get('password'))
            user.first_name = request.POST.get('user_code')
            user.save()
            profile = form.save(commit=False)
            profile.save()

            profile_image = request.FILES.get('profile_image', False)
            if profile_image:
                if profile.image:
                    image = Image.objects.get(pk=profile.image_id)
                    image.delete()

                new_image = Image()
                new_image.image.save(profile_image.name, profile_image)
                new_image.save()

                profile.image = new_image
                profile.save()
    else:
        form = ProfileForm()
    
    store_list = [
        ['1', 'Store A'],
        ['2', 'Store B']
    ]
    profile_list = Profile.objects.all().values('id', 'nickname')
    return render(request, 'profile_form.html', {'form': form, 
                                                'media_url': s.MEDIA_URL, 
                                                'store_list': store_list,
                                                'profile_list': profile_list})

@login_required
def profile_edit(request, profile_id):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid:
            user = User.objects.create_user(username=request.POST.get('tel'))
            if user:
                user.first_name = request.POST.get('user_code')
                user.set_password(request.POST.get('password'))
                user.save()
            profile = form.save(commit=False)
            profile.user = user
            profile.save()

            profile_image = request.FILES.get('profile_image', False)
            if profile_image:
                if profile.image:
                    image = Image.objects.get(pk=profile.image_id)
                    image.delete()

                new_image = Image()
                new_image.image.save(profile_image.name, profile_image)
                new_image.save()

                profile.image = new_image
                profile.save()
            return render(request, 'profile_list.html')
        else:
            print(form.errors)

    profile = Profile.objects.get(pk=profile_id)
    form = ProfileForm(instance=profile)
    
    store_list = [
        ['1', 'Store A'],
        ['2', 'Store B']
    ]
    profile_list = Profile.objects.all().values('id', 'nickname')
    return render(request, 'profile_form.html', {'form': form, 
                                                'media_url': s.MEDIA_URL, 
                                                'store_list': store_list,
                                                'profile_list': profile_list,
                                                'profile': profile})

@login_required
def profile_delete(request, profile_id):
    try:
        profile = Profile.objects.get(pk=profile_id)
        profile.is_hidden = 1
        profile.update_date = datetime.datetime.today()
        profile.save()
    except Exception as e:
        print(e)
    return render(request, 'profile_list.html')