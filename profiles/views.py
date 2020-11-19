import datetime
import json
from django.conf import settings as s
from django.contrib import messages
from django.db.models import Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.urls import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .forms import ProfileForm, ImageUploadForm
from .models import Address, Profile, FinancialAccount, UserSale, \
    UserCommision, MonthlyPayment
from products.models import ProductCategory
from utilities.constants import AUTHORITY_TYPE
from prefectures.models import Prefecture
from images.models import Image


@login_required    
def home_load(request):
    """
    Method to redirect to home/dashboard.
    """
    return render(request, 'base.html')

@login_required 
def listing_home_load(request):
    """
    Method to redirect to listing home/dashboard.
    """
    return render(request, 'base.html')

@login_required 
def sales_listing_site(request):
    """
    Method to redirect to listing home/dashboard.
    """

    request.session['login_type'] = 'SELLER'
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

                    profile = Profile.objects.filter(user_id=user.id, is_hidden=False).first()
                    if profile:
                        profile.password = password
                        profile.save()

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

    state = ""
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                profile = Profile.objects.filter(is_hidden=False, user_id=user.id).first()
                if profile and profile.authority_id == AUTHORITY_TYPE['MASTER']:
                    login(request, user)
                    request.session['login_profile_id'] = profile.id
                    request.session['login_authority_id'] = profile.authority_id
                    request.session['login_type'] = 'MASTER'
                    return HttpResponsePermanentRedirect(reverse('home_load'))
                else:
                    state = "User is not a Master Account"
                    return render(request, 'master_login.html', {'state': state})
            else:
                state = "Check username & password"
                return render(request, 'master_login.html', {'state': state})
        except Exception as e:
            state = "Check username & password"
            print(e)
            return render(request, 'master_login.html', {'state': state})

    return render(request, 'master_login.html', {'state': state})


def login_sales(request):
    """
    Method to sales login.
    """
    
    state = ""
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                profile = Profile.objects.filter(is_hidden=False, user_id=user.id).first()
                if profile.is_seller:
                    login(request, user)
                    request.session['login_profile_id'] = profile.id
                    request.session['login_authority_id'] = profile.authority_id
                    request.session['login_type'] = 'SELLER'
                    return redirect('listing_home_load')
                else:
                    state = "User is not Seller Account"
                    return render(request, 'sales_login.html', {'state': state})
            else:
                state = "Check username & password"
                return render(request, 'sales_login.html', {'state': state})
        except Exception as e:
            print(e)
            state = "Check username & password"
            return render(request, 'sales_login.html', {'state': state})

    return render(request, 'sales_login.html', {'state': state})

def logout_user(request):
    """
    Method to logout.
    """

    login_type_was = request.session['login_type']
    logout(request)
    if login_type_was == 'MASTER':
        request.session['login_type'] = 'MASTER'
        return render(request, 'master_login.html')
    else:
        request.session['login_type'] = 'SELLER'
        return render(request, 'sales_login.html')

@login_required
def profile_list(request):
    """
    Method to redirect to profile list page.
    """

    if request.session['login_type'] == 'MASTER':
        return render(request, 'profile_list.html')
    else:
        return render(request, '404.html')


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
        if profile_list:
            profile_list = profile_list.filter(is_approved=False)
        else:
            profile_list = Profile.objects.filter(is_approved=False, is_hidden=False).order_by('authority_id')
        
    records_total = profile_list.count()

    if search:  # Filter data base on search
        profile_list = profile_list.filter(Q(real_name__icontains=search)).order_by('-real_name')

    # All data
    records_filtered = profile_list.count()
    # Order by list_limit base on order_dir and order_column
    order_column = request.GET['order[0][column]']
    column_name = ""
    if order_column == "2":
        column_name = "real_name"
    
    order_dir = request.GET['order[0][dir]']
    list = []
    if order_dir == "asc":
        list = profile_list.order_by(column_name)[int(start):(int(start) + int(length))]
    elif order_dir == "desc":
        list = profile_list.order_by('-' + column_name)[int(start):(int(start) + int(length))]

    array = []
    introducer_list = Profile.objects.filter(is_hidden=False)
    i = 0
    for field in list:
        i = i + 1
        store_total = introducer_list.filter(introducer_id=field.id, authority_id=AUTHORITY_TYPE['STORE']).count()
        user_total = introducer_list.filter(introducer_id=field.id, authority_id=AUTHORITY_TYPE['GENERAL']).count()
        data = {"no": str(i),
                "id": str(field.id),
                "type": field.authority.name,
                "real_name": field.real_name,
                "store_total": str(store_total),
                "user_total": str(user_total)
                }
        array.append(data)

    content = {"draw": draw, "data": array, "recordsTotal": records_total, "recordsFiltered": records_filtered}
    json_content = json.dumps(content, ensure_ascii=False)
    return HttpResponse(json_content, content_type='application/json')


# @login_required
def ClientList__asJson(request):
    """
    Method to get client list as JSON.
    """

    draw = request.GET['draw']
    start = request.GET['start']
    length = request.GET['length']
    search = request.GET['search[value]']

    profile_id = int(request.GET.get('profile_id'))
    auth_type = eval(request.GET.get('filter_str'))

    profile_list = Profile.objects.filter(introducer_id=profile_id, is_hidden=False).order_by('authority_id')

    if(len(auth_type)):
        profile_list = profile_list.filter(authority_id__in=auth_type)
        
    records_total = profile_list.count()

    if search:  # Filter data base on search
        profile_list = profile_list.filter(Q(real_name__icontains=search) | Q(created__icontains=search)).order_by('-real_name')

    # All data
    records_filtered = profile_list.count()
    # Order by list_limit base on order_dir and order_column
    order_column = request.GET['order[0][column]']
    column_name = ""
    if order_column == "2":
        column_name = "real_name"
    if order_column == "3":
        column_name = "created"
    
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
                "real_name": field.real_name,
                "created": field.created.strftime("%Y-%m-%d")
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

@login_required
def profile_add(request):
    """
    Method to add new user profile.
    """

    if request.session['login_type'] == 'MASTER':
        if request.method == 'POST':
            form = ProfileForm(request.POST)
            if form.is_valid:
                try:
                    user = User.objects.create_user(request.POST.get('tel'), 'test@test.com', request.POST.get('password'))
                    user.first_name = request.POST.get('user_code')
                    user.save()
                    profile = form.save(commit=False)
                    profile.user = user
                    profile.user_code = request.POST.get('user_code')
                    if request.POST.get('birthday'):
                        profile.birthday = request.POST.get('birthday')
                    
                    if request.POST.get('is_seller') == '1':
                        profile.is_seller = True
                    else:
                        profile.is_seller = False

                    if profile.authority_id in (AUTHORITY_TYPE['AMBASSADOR'], AUTHORITY_TYPE['GENERAL'],
                        AUTHORITY_TYPE['MASTER'], AUTHORITY_TYPE['SPECIAL']):
                        profile.is_approved = True
                    else:
                        profile.is_approved = False
                    
                    if profile.authority_id == AUTHORITY_TYPE['AMBASSADOR']:
                        if request.POST.get('general_store') and request.POST.get('general_store') != '' and request.POST.get('general_store') != None:
                            profile.introducer_id = int(request.POST.get('general_store'))
                    
                    elif profile.authority_id in (AUTHORITY_TYPE['STORE'], AUTHORITY_TYPE['GENERAL']):
                        if request.POST.get('introducer') and request.POST.get('introducer') != '' and request.POST.get('introducer') != None:
                            profile.introducer_id = int(request.POST.get('introducer'))

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
                    messages.add_message(request, messages.ERROR, e, extra_tags='profile_add')
        else:
            form = ProfileForm()
        
        store_list = Profile.objects.filter(is_hidden=False, authority_id=AUTHORITY_TYPE['SPECIAL']).values('id', 'real_name')
        profile_list = list(Profile.objects.filter(is_hidden=False).values_list('id', 'real_name', 'authority_id'))
        return render(request, 'profile_form.html', {'form': form, 
                                                    'media_url': s.MEDIA_URL, 
                                                    'store_list': store_list,
                                                    'profile_list': profile_list})
    else:
        return render(request, '404.html')


@login_required
def profile_edit(request, profile_id):
    """
    Method to edit a user profile.
    """

    if request.session['login_type'] == 'MASTER':
        if request.method == 'POST':
            profile = Profile.objects.get(pk=profile_id)
            form = ProfileForm(request.POST, instance=profile)
            if form.is_valid:
                try:
                    user = User.objects.filter(pk=profile.user_id).first()
                    if user:
                        if user.username != request.POST.get('tel'):
                            user.username = request.POST.get('tel')
                            user.save()
                        if user.first_name != request.POST.get('real_name'):
                            user.first_name = request.POST.get('real_name')
                            user.save()
                        if request.POST.get('password') != '' and request.POST.get('password') != None:
                            user.set_password(request.POST.get('password'))
                            user.save()
                    else:
                        if request.POST.get('password') != '' and request.POST.get('password') != None:
                            user = User.objects.create_user(request.POST.get('tel'), 'test@test.com', request.POST.get('password'))
                            user.first_name = request.POST.get('real_name')
                            user.save()
                    
                    profile = form.save(commit=False)
                    if user:
                        profile.user_id = user.id
                    else:
                        profile.user_id = request.POST.get('user_id')
                    
                    if profile.authority_id == AUTHORITY_TYPE['AMBASSADOR']:
                        if request.POST.get('general_store') and request.POST.get('general_store') != '' and request.POST.get('general_store') != None:
                            profile.introducer_id = int(request.POST.get('general_store'))
                    
                    elif profile.authority_id in (AUTHORITY_TYPE['STORE'], AUTHORITY_TYPE['GENERAL']):
                        if request.POST.get('introducer') and request.POST.get('introducer') != '' and request.POST.get('introducer') != None:
                            profile.introducer_id = int(request.POST.get('introducer'))

                    if request.POST.get('birthday'):
                        profile.birthday = request.POST.get('birthday')

                    if request.POST.get('is_seller') == '1':
                        profile.is_seller = True
                    else:
                        profile.is_seller = False
                    if request.POST.get('is_approved') == '1':
                        profile.is_approved = True
                    else:
                        profile.is_approved = False

                    profile.modified = datetime.datetime.now()
                    profile.save()
                    
                    profile_image = request.FILES.get('profile_image', False)
                    if profile_image:
                        if profile.image:
                            image = Image.objects.get(pk=profile.image_id)
                            image.is_hidden = True
                            image.modified = datetime.datetime.now()
                            image.save()

                        new_image = Image()
                        new_image.image.save(profile_image.name, profile_image)
                        new_image.save()

                        profile.image = new_image
                        profile.save()

                    active = request.POST.get('active_checkbox', '') == 'on'
                    if not active:
                        profile.is_hidden = True
                    
                    profile.save()

                    return render(request, 'profile_list.html')
                except Exception as e:
                    print(e)
                    messages.add_message(request, messages.ERROR, e, extra_tags='profile_edit')
            else:
                print(form.errors)

        profile = Profile.objects.get(pk=profile_id)
        form = ProfileForm(instance=profile)
        
        store_list = Profile.objects.filter(is_hidden=False, authority_id=AUTHORITY_TYPE['SPECIAL']).exclude(id=profile_id).values('id', 'real_name')
        profile_list = list(Profile.objects.filter(is_hidden=False).exclude(id=profile_id).values_list('id', 'real_name', 'authority_id'))
        prefecture_list = list(Prefecture.objects.filter(is_hidden=False, is_enable=True).order_by('id').values_list('id', 'name'))
        category_list = list(ProductCategory.objects.filter(is_hidden=False).order_by('id').values_list('id', 'name'))
        return render(request, 'profile_form.html', {'form': form, 
                                                    'media_url': s.MEDIA_URL, 
                                                    'store_list': store_list,
                                                    'profile_list': profile_list,
                                                    'profile': profile,
                                                    'category_list': category_list,
                                                    'prefecture_list': prefecture_list})
    else:
        return render(request, '404.html')


@login_required
@csrf_exempt
def profile_delete(request, profile_id):
    """
    Method to delete a user profile.
    """

    if request.session['login_type'] == 'MASTER':
        try:
            profile = Profile.objects.get(pk=profile_id)
            profile.is_hidden = 1
            profile.modified = datetime.datetime.now()
            profile.save()
            
            if profile.image:
                image = Image.objects.get(pk=profile.image_id)
                image.is_hidden = True
                image.modified = datetime.datetime.now()
                image.save()
        except Exception as e:
            print(e)
        return render(request, 'profile_list.html')
    else:
        return render(request, '404.html')

    
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
            
            # if it is default then remove other from default
            if shipping_info.is_default:
                Address.objects.filter(user_id=profile_id).exclude(id=shipping_info.id).update(is_default=False)

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
                "address1": field.address1,
                "address2": field.address2,
                "zip1": field.zip1,
                "prefecture": field.prefecture.name,
                "prefecture_id": field.prefecture.id,
                "tel": field.tel
                }
        array.append(data)

    content = {"draw": draw, "data": array, "recordsTotal": records_total, "recordsFiltered": records_filtered}
    json_content = json.dumps(content, ensure_ascii=False)
    return HttpResponse(json_content, content_type='application/json')


def validate_user_phone(request, profile_id):
    """
    Method to verify duplcate user.
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


def check_for_duplicate(request, type, value):
    """
    Method to verify duplcate info.
    """

    message = 'Error'
    try:
        user = None
        if type == 'tel':
            user = Profile.objects.filter(tel=value).first()
        elif type == 'id':
            user = Profile.objects.filter(user_code=value).first()

        if user:
            message = 'Success'
    except Exception as e:
        print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")


def get_data(request, year, month):
    """
    Method to get user sales & commission data.
    """

    data = {
        "sales": 0,
        "commission": 0,
        "total": 0
    }
    try:
        profile_id = request.session['login_profile_id']
        auth_type = request.session['login_authority_id']

        if auth_type == AUTHORITY_TYPE['MASTER']:
            sales_list = UserSale.objects.filter(is_hidden=False,
                                    user__authority_id=auth_type,
                                    year=year, month=month)\
                    .aggregate(sale_amount=Coalesce(Sum('sales_amount'), Value(0)))
            commission_list = UserCommision.objects.filter(is_hidden=False,
                                    user__authority_id=auth_type,
                                    year=year, month=month)\
                    .aggregate(com_amount=Coalesce(Sum('amount'), Value(0)))
        else:
            sales_list = UserSale.objects.filter(is_hidden=False,
                                    user_id=profile_id,
                                    year=year, month=month)\
                    .aggregate(sale_amount=Coalesce(Sum('sales_amount'), Value(0)))
            commission_list = UserCommision.objects.filter(is_hidden=False,
                                    user_id=profile_id,
                                    year=year, month=month)\
                    .aggregate(com_amount=Coalesce(Sum('amount'), Value(0)))

        data = {
            "sales": sales_list.get('sale_amount', 0),
            "commission": commission_list.get('com_amount', 0),
            "total": sales_list.get('sale_amount', 0) + commission_list.get('com_amount', 0)
        }
    except Exception as e:
        print(e)

    context = { 'data': data }
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
    Method to redirect to shipping entry form.
    """
    return render(request, 'shipping_form.html')

# @login_required
def shipping_table(request):
    """
    Method to redirect to shipping.
    """
    return render(request, 'shipping_info_tab.html')

# @login_required
def sales_list(request):
    """
    Method to redirect to sales list page.
    """

    if request.session['login_type'] == 'MASTER':
        return render(request, 'sales_list.html')
    else:
        return render(request, '404.html')

# @login_required
def payment_list(request):
    """
    Method to redirect to payment list page.
    """

    if request.session['login_type'] == 'MASTER':
        return render(request, 'payment_list.html')
    else:
        return render(request, '404.html')


# @login_required
def listing_sales_list(request):
    """
    Method to redirect to sales list page.
    """

    if request.session['login_type'] == 'SELLER':
        return render(request, 'listing_sales_list.html')
    else:
        return render(request, '404.html')

def get_product_form(request):
    """
    Method to get product form page.
    """

    return render(request, 'item_form.html')

def get_product_list_page(request):
    """
    Method to get product list page.
    """

    return render(request, 'item_info_tab.html')


def PaymentList__asJson(request):
    """
    Method to get payment list as JSON.
    """

    draw = request.GET['draw']
    start = request.GET['start']
    length = request.GET['length']
    search = request.GET['search[value]']

    auth_type = eval(request.GET.get('auth_str'))
    status_type = eval(request.GET.get('status_str'))
    month = eval(request.GET.get('month'))
    year = eval(request.GET.get('year'))

    payment_list = MonthlyPayment.objects.filter(is_hidden=False, year=year, month=month).order_by('user__real_name')
    if len(auth_type):
        payment_list = payment_list.filter(user__authority_id__in=auth_type)
    if len(status_type):
        payment_list = payment_list.filter(status__in=status_type)
        
    records_total = payment_list.count()

    if search:  # Filter data base on search
        payment_list = payment_list.filter(Q(user__real_name__icontains=search))

    # All data
    records_filtered = payment_list.count()
    # Order by list_limit base on order_dir and order_column
    order_column = request.GET['order[0][column]']
    column_name = ""
    if order_column == "1":
        column_name = "name"
    
    # order_dir = request.GET['order[0][dir]']
    # list = []
    # if order_dir == "asc":
    #     list = payment_list.order_by(column_name)[int(start):(int(start) + int(length))]
    # elif order_dir == "desc":
    #     list = payment_list.order_by('-' + column_name)[int(start):(int(start) + int(length))]

    array = []
    i = 0
    for field in payment_list:
        i = i + 1
        bank_info = FinancialAccount.objects.filter(is_hidden=False, user_id=field.user_id)
        if bank_info.exists():
            bank_info = bank_info.last()
        else:
            bank_info = None
        data = {
            "no": str(i),
            "name": field.user.real_name,
            "bank_name": bank_info.financial_code + ' ' + bank_info.financial_name if bank_info else '',
            "branch_name": bank_info.branch_code + ' ' + bank_info.branch_name if bank_info else '',
            "account_number": bank_info.account_number if bank_info else '',
            "account_name": bank_info.account_name if bank_info else '',
            "amount": str(field.amount),
            "paid_date": field.paid_date.strftime('%Y-%m-%d') if field.paid_date else '',
            "id": str(field.id),
        }
        array.append(data)

    content = {"draw": draw, "data": array, "recordsTotal": records_total, "recordsFiltered": records_filtered}
    json_content = json.dumps(content, ensure_ascii=False)
    return HttpResponse(json_content, content_type='application/json')


@csrf_exempt
def update_payment(request):
    """
    Method to update payment info.
    """

    message = 'Error'
    if request.method == 'POST':
        payment_id = request.POST.get('payment_id')
        date = request.POST.get('payment_date')
        try:
            payment = MonthlyPayment.objects.get(pk=payment_id)
            payment.paid_date = date
            payment.status = True
            payment.modified = datetime.datetime.now()
            payment.save()

            message = 'Success'
        except Exception as e:
            print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")