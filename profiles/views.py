from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.urls import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .forms import ProfileForm, ImageUploadForm
from .models import Address, Profile, FinancialAccount
from prefectures.models import Prefecture
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

    if request.method == 'POST':
        try:
            username = request.POST.get('user_phone')
            password = request.POST.get('new_pass')
            user = User.objects.filter(username=username).first()
            if user:
                if password != '' and password != None:
                    user.set_password(password)
                    user.save()

                    user = authenticate(username=username, password=password)
                    if user is not None:
                        login(request, user)
                        return HttpResponsePermanentRedirect(reverse('home_load'))
        except Exception as e:
            print(e)

    return render(request, 'password-reset.html')

def login_master(request):
    """
    Method to master login.
    """

    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponsePermanentRedirect(reverse('home_load'))
            else:
                return render(request, 'master_login.html')
        except Exception as e:
            print(e)
            return render(request, 'master_login.html')

    return render(request, 'master_login.html')

def login_sales(request):
    """
    Method to sales login.
    """
    
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponsePermanentRedirect(reverse('home_load'))
            else:
                return render(request, 'sales_login.html')
        except Exception as e:
            print(e)
            return render(request, 'sales_login.html')

    return render(request, 'sales_login.html')

def logout_user(request):
    """
    Method to logout.
    """
    logout(request)
    return render(request, 'master_login.html')

# @login_required
def profile_list(request):
    """
    Method to redirect to profile list page.
    """

    return render(request, 'profile_list.html')

# @login_required
def ProfileList__asJson(request):
    """
    Method to get profile list as JSON.
    """

    draw = request.GET['draw']
    start = request.GET['start']
    length = request.GET['length']
    search = request.GET['search[value]']

    auth_type = eval(request.GET.get('filter_str'))

    profile_list = Profile.objects.filter(authority_id__in=auth_type, is_hidden=False).order_by('authority_id')
    if 0 in auth_type:
        profile_list = profile_list.filter(is_approved=False)
        
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
# def upload_profile_image(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             m = form.save(commit=False)
#             m.image = form.cleaned_data.get('profile_image')
#             m.save()
#             json_content = json.dumps({'image': m}, ensure_ascii=False)
#             return HttpResponse(json_content, content_type='application/json')

# @login_required
def profile_add(request):
    """
    Method to add new user profile.
    """

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid:
            try:
                user = User.objects.create_user(request.POST.get('tel'), 'test@test.com', request.POST.get('password'))
                user.first_name = request.POST.get('user_code')
                user.save()
                profile = form.save(commit=False)
                profile.user = user
                if request.POST.get('introducer') and request.POST.get('introducer') != '' and request.POST.get('introducer') != None:
                    profile.indroducer = int(request.POST.get('introducer'))
                if request.POST.get('general_store') and request.POST.get('general_store') != '' and request.POST.get('general_store') != None:
                    profile.indroducer = int(request.POST.get('general_store'))
                profile.user_code = request.POST.get('user_code')
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
    
    store_list = Profile.objects.filter(is_hidden=False, authority_id=2).values('id', 'nickname') #authority_id=2 ambassador
    profile_list = Profile.objects.filter(is_hidden=False).exclude(authority_id=2).values('id', 'nickname')
    return render(request, 'profile_form.html', {'form': form, 
                                                'media_url': s.MEDIA_URL, 
                                                'store_list': store_list,
                                                'profile_list': profile_list})

# @login_required
def profile_edit(request, profile_id):
    """
    Method to edit a user profile.
    """

    if request.method == 'POST':
        profile = Profile.objects.get(pk=profile_id)
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid:
            try:
                user = User.objects.filter(username=request.POST.get('tel')).first()
                if user:
                    if request.POST.get('password') != '' and request.POST.get('password') != None:
                        user.first_name = request.POST.get('nickname')
                        user.set_password(request.POST.get('password'))
                        user.save()
                else:
                    if request.POST.get('password') != '' and request.POST.get('password') != None:
                        user = User.objects.create_user(request.POST.get('tel'), 'test@test.com', request.POST.get('password'))
                        user.first_name = request.POST.get('nickname')
                        user.save()
                
                profile = form.save(commit=False)
                if user:
                    profile.user_id = user.id
                else:
                    profile.user_id = request.POST.get('user_id')
                if request.POST.get('introducer') and request.POST.get('introducer') != '' and request.POST.get('introducer') != None:
                    profile.indroducer = int(request.POST.get('introducer'))
                if request.POST.get('general_store') and request.POST.get('general_store') != '' and request.POST.get('general_store') != None:
                    profile.indroducer = int(request.POST.get('general_store'))
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

                    active = request.POST.get('active_checkbox', '') == 'on'
                    if not active:
                        profile.is_hidden = True
                    
                    profile.modified = datetime.datetime.now()
                    profile.save()

                    return render(request, 'profile_list.html')
            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR, e, extra_tags='profile_edit')
        else:
            print(form.errors)

    profile = Profile.objects.get(pk=profile_id)
    form = ProfileForm(instance=profile)
    
    store_list = Profile.objects.filter(is_hidden=False, authority_id=2).exclude(id=profile_id).values('id', 'nickname') #authority_id=2 ambassador
    profile_list = Profile.objects.filter(is_hidden=False).exclude(id=profile_id).exclude(authority_id=2).values('id', 'nickname')
    prefecture_list = list(Prefecture.objects.filter(is_hidden=False, is_enable=True).order_by('name').values_list('id', 'name'))
    return render(request, 'profile_form.html', {'form': form, 
                                                'media_url': s.MEDIA_URL, 
                                                'store_list': store_list,
                                                'profile_list': profile_list,
                                                'profile': profile,
                                                'prefecture_list': prefecture_list})

# @login_required
@csrf_exempt
def profile_delete(request, profile_id):
    """
    Method to delete a user profile.
    """

    try:
        profile = Profile.objects.get(pk=profile_id)
        profile.is_hidden = 1
        profile.modified = datetime.datetime.now()
        profile.save()
    except Exception as e:
        print(e)
    return render(request, 'profile_list.html')

    
# @login_required
@csrf_exempt
def get_financial_info(request):
    """
    Method get a user profile account information.
    """

    context = {
        'bank_name': '',
        'bank_code': '',
        'account_type': '',
        'branch_code': '',
        'branch_name': '',
        'account_holder': '',
        'account_number': '',
    }
    if request.method == 'POST':
        try:
            profile_id = request.POST.get('profile_id')
            financial_info = FinancialAccount.objects.filter(user_id=profile_id, is_hidden=False)
            if financial_info:
                financial_info = financial_info.last()
                context = {
                    'bank_name': str(financial_info.financial_name),
                    'bank_code': str(financial_info.financial_code),
                    'account_type': str(financial_info.account_type),
                    'branch_code': str(financial_info.branch_code),
                    'branch_name': str(financial_info.branch_name),
                    'account_holder': str(financial_info.account_name),
                    'account_number': str(financial_info.account_number),
                }
        except Exception as e:
            print(e)

    return HttpResponse(json.dumps(context), content_type="application/json")


# @login_required
@csrf_exempt
def update_financial_info(request):
    """
    Method update a user profile account information.
    """

    message = 'Error'
    if request.method == 'POST':
        try:
            profile_id = request.POST.get('profile_id')
            bank_name = request.POST.get('bank_name')
            bank_code = request.POST.get('bank_code')
            branch_code = request.POST.get('branch_code')
            branch_name = request.POST.get('branch_name')
            account_holder = request.POST.get('account_holder')
            account_number = request.POST.get('account_number')
            account_type = int(request.POST.get('account_type'))

            financial_info = FinancialAccount.objects.filter(user_id=profile_id, is_hidden=False)
            if financial_info:
                financial_info = financial_info.last()
                financial_info.financial_name = bank_name
                financial_info.financial_code = bank_code
                financial_info.branch_code = branch_code
                financial_info.branch_name = branch_name
                financial_info.account_number = account_number
                financial_info.account_name = account_holder
                financial_info.account_type = account_type

                financial_info.modified = datetime.datetime.now()
                financial_info.save()
            else:
                financial_info = FinancialAccount()
                financial_info.user_id = profile_id
                financial_info.financial_name = bank_name
                financial_info.financial_code = bank_code
                financial_info.branch_code = branch_code
                financial_info.branch_name = branch_name
                financial_info.account_number = account_number
                financial_info.account_name = account_holder
                financial_info.account_type = account_type

                financial_info.save()

            message = 'Success'
        except Exception as e:
            print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")

@csrf_exempt
def get_shipping_info(request):
    """
    Method get a user shipping information.
    """

    context = {
        'destination_name': '',
        'full_name': '',
        'zip_code': '',
        'address1': '',
        'address2': '',
        'add_tel': '',
        'prefecture': '',
        'is_default': '0'
    }
    if request.method == 'POST':
        try:
            shipping_id = request.POST.get('shipping_id')
            address_info = Address.objects.filter(id=shipping_id, is_hidden=False)
            if address_info:
                address_info = address_info.last()
                context = {
                    'destination_name': str(address_info.address_name),
                    'full_name': str(address_info.name),
                    'zip_code': str(address_info.zip1),
                    'address1': str(address_info.address1),
                    'address2': str(address_info.address2),
                    'add_tel': str(address_info.tel),
                    'prefecture': str(address_info.prefecture_id),
                    'is_default': '1' if address_info.is_default else '0'
                }
        except Exception as e:
            print(e)

    return HttpResponse(json.dumps(context), content_type="application/json")


# @login_required
@csrf_exempt
def update_shipping_info(request):
    """
    Method update a user shipping information.
    """

    message = 'Error'
    if request.method == 'POST':
        try:
            profile_id = request.POST.get('profile_id')
            shipping_id = request.POST.get('shipping_id')
            address_name = request.POST.get('address_name')
            name = request.POST.get('name')
            zip1= request.POST.get('zip_code')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            tel = request.POST.get('add_tel')
            prefecture = int(request.POST.get('prefecture'))
            is_default = int(request.POST.get('is_default'))

            if shipping_id != '':
                shipping_info = Address.objects.filter(id=shipping_id, user_id=profile_id, is_hidden=False)

                if shipping_info:
                    shipping_info = shipping_info.last()
                    shipping_info.address_name = address_name
                    shipping_info.name = name
                    shipping_info.address1 = address1
                    shipping_info.address2 = address2
                    shipping_info.zip1 = zip1
                    shipping_info.tel = tel
                    shipping_info.prefecture_id = prefecture
                    shipping_info.is_default = is_default

                    shipping_info.modified = datetime.datetime.now()
                    shipping_info.save()
            else:
                shipping_info = Address()
                shipping_info.user_id = profile_id
                shipping_info.address_name = address_name
                shipping_info.name = name
                shipping_info.address1 = address1
                shipping_info.address2 = address2
                shipping_info.zip1 = zip1
                shipping_info.tel = tel
                shipping_info.prefecture_id = prefecture
                shipping_info.is_default = is_default

                shipping_info.save()

            message = 'Success'
        except Exception as e:
            print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")


# @login_required
@csrf_exempt
def delete_shipping_info(request):
    """
    Method to delete a shipping info.
    """

    message = 'Error'
    if request.method == 'POST':
        shipping_id = request.POST.get('shipping_id')
        try:
            shipping = Address.objects.get(pk=shipping_id)
            shipping.is_hidden = 1
            shipping.modified = datetime.datetime.now()
            shipping.save()

            message = 'Success'
        except Exception as e:
            print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")


# @login_required
def ShippingList__asJson(request):
    """
    Method to get profile list as JSON.
    """

    draw = request.GET['draw']
    start = request.GET['start']
    length = request.GET['length']
    search = request.GET['search[value]']

    user_id = request.GET.get('user_id')

    shipping_list = Address.objects.filter(user_id=user_id, is_hidden=False).order_by('name')
        
    records_total = shipping_list.count()

    if search:  # Filter data base on search
        shipping_list = shipping_list.filter(Q(name__icontains=search)|Q(address_name__icontains=search)|Q(tel__icontains=search)).order_by('-name')

    # All data
    records_filtered = shipping_list.count()
    # Order by list_limit base on order_dir and order_column
    order_column = request.GET['order[0][column]']
    column_name = ""
    if order_column == "1":
        column_name = "address_name"
    if order_column == "2":
        column_name = "name"
    if order_column == "4":
        column_name = "tel"
    
    order_dir = request.GET['order[0][dir]']
    list = []
    if order_dir == "asc":
        list = shipping_list.order_by(column_name)[int(start):(int(start) + int(length))]
    elif order_dir == "desc":
        list = shipping_list.order_by('-' + column_name)[int(start):(int(start) + int(length))]

    array = []
    i = 0
    for field in list:
        i = i + 1
        data = {"no": str(i),
                "id": str(field.id),
                "address_name": field.address_name,
                "name": field.name,
                "address": field.address1 + '</br>' + field.address2 + ' Zip:' + field.zip1,
                "tel": field.tel
                }
        array.append(data)

    content = {"draw": draw, "data": array, "recordsTotal": records_total, "recordsFiltered": records_filtered}
    json_content = json.dumps(content, ensure_ascii=False)
    return HttpResponse(json_content, content_type='application/json')


def validate_user_phone(request, profile_id):
    """
    Method to delete a shipping info.
    """

    message = 'Error'
    try:
        user = User.objects.filter(username=profile_id).first()
        if user:
            message = 'Success'
    except Exception as e:
        print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")

# @login_required
def salon_form(request):
    """
    Method to redirect to salon entry form.
    """
    return render(request, 'salon_form.html')

# @login_required
def salon_table(request):
    """
    Method to redirect to salon.
    """
    return render(request, 'salon_info_tab.html')

# @login_required
def shipping_form(request):
    """
    Method to redirect to salon entry form.
    """
    return render(request, 'shipping_form.html')

# @login_required
def shipping_table(request):
    """
    Method to redirect to salon.
    """
    return render(request, 'shipping_info_tab.html')