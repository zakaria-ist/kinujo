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
from django.contrib import messages
from django.db.models import Q

# @login_required
def home_load(request):
    """
    Method to redirect to home/dashboard.
    """
    return render(request, 'base.html')

def pass_reset(request):
    """
    Method to redirect to password reset page.
    """
    return render(request, 'password-reset.html')

def reset_password(request):
    """
    Method to update new password.
    """
    return render(request, 'login.html')

def login_user(request):
    """
    Method to login.
    """
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
    """
    Method to logout.
    """
    logout(request)
    return render(request, 'login.html')

# @login_required
def profile_list(request):
    """
    Method to redirect to profile list page.
    """

    return render(request, 'profile_list.html')

# @login_required
def ProfileList__asJson(request, auth_type=None):
    """
    Method to get profile list as JSON.
    """

    draw = request.GET['draw']
    start = request.GET['start']
    length = request.GET['length']
    search = request.GET['search[value]']
    if auth_type == None:
        auth_type = 1;

    profile_list = Profile.objects.filter(authority_id__in=auth_type).order_by('authority_id')
    records_total = profile_list.count()

    if search:  # Filter data base on search
        profile_list = profile_list.filter(Q(nickname__icontains=search)).order_by('-nickname')

    # All data
    records_filtered = profile_list.count()
    # Order by list_limit base on order_dir and order_column
    order_column = request.GET['order[0][column]']
    column_name = ""
    if order_column == "2":
        column_name = "nickname"
    
    order_dir = request.GET['order[0][dir]']
    list = []
    if order_dir == "asc":
        list = profile_list.order_by(column_name)[int(start):(int(start) + int(length))]
    elif order_dir == "desc":
        list = profile_list.order_by('-' + column_name)[int(start):(int(start) + int(length))]

    array = []
    i = 0
    for field in list:
        i = i + 1
        data = {"no": str(i),
                "id": str(field.id),
                "type": field.authority.name,
                "nickname": field.nickname,
                "store_total": '0',
                "user_total": '0'
                }
        array.append(data)

    content = {"draw": draw, "data": array, "recordsTotal": records_total, "recordsFiltered": records_filtered}
    json_content = json.dumps(content, ensure_ascii=False)
    return HttpResponse(json_content, content_type='application/json')

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
            try:
                user = User.objects.create_user(request.POST.get('tel'), 'test@test.com', request.POST.get('password'))
                user.first_name = request.POST.get('user_code')
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
            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR, e, extra_tags='profile_add')
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

# @login_required
def profile_edit(request, profile_id):
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid:
            try:
                user = User.objects.filter(username=request.POST.get('tel')).first()
                if user:
                    user.first_name = request.POST.get('user_code')
                    user.set_password(request.POST.get('password'))
                    user.save()
                else:
                    user = User.objects.create_user(request.POST.get('tel'), 'test@test.com', request.POST.get('password'))
                    user.first_name = request.POST.get('user_code')
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
            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR, e, extra_tags='profile_edit')
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