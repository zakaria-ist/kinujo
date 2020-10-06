from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.urls import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Profile
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
    
    #     order_list = Order.objects.filter(is_hidden=0, company_id=company_id, order_type=order_type).order_by('-document_number')

    # records_total = order_list.count()

    # if search:  # Filter data base on search
    #     if int(order_type) == dict(ORDER_TYPE)['PURCHASE INVOICE']:
    #         order_list = order_list.filter(Q(update_date__icontains=search) | Q(document_date__icontains=search) | Q(
    #             document_number__icontains=search) | Q(update_date__contains=search) | Q(
    #             customer__name__icontains=search) | Q(supplier__name__icontains=search) | Q(balance__icontains=search) | Q(
    #             reference_number__icontains=search) | Q(total__icontains=search)).order_by('-document_date')

    # All data
    # records_filtered = order_list.count()
    # # Order by list_limit base on order_dir and order_column
    # order_column = request.GET['order[0][column]']
    # column_name = ""
    # if order_column == "1":
    #     column_name = "update_date"
    # elif order_column == "2":
    #     column_name = "id"
    # elif order_column == "3":
    #     column_name = "document_date"
    # elif order_column == "4":
    #     column_name = "document_number"
    # elif order_column == "5":
    #     column_name = "reference_number"
    # elif order_column == "6":
    #     column_name = get_cust_supp_column_name(int(order_type))
    # elif order_column == "7":
    #     column_name = "total"
    # elif order_column == "8":
    #     column_name = "status"

    # order_dir = request.GET['order[0][dir]']
    # list = []
    # if order_dir == "asc":
    #     if int(order_type) == dict(ORDER_TYPE)['PURCHASE INVOICE']:
    #         list = order_list.order_by('document_date', column_name)[int(start):(int(start) + int(length))]
    #     else:
    #         list = order_list.order_by('document_number', column_name)[int(start):(int(start) + int(length))]
    # elif order_dir == "desc":
    #     if int(order_type) == dict(ORDER_TYPE)['PURCHASE INVOICE']:
    #         list = order_list.order_by('-document_date', '-' + column_name)[int(start):(int(start) + int(length))]
    #     else:
    #         list = order_list.order_by('-document_number', '-' + column_name)[int(start):(int(start) + int(length))]

    # # Create data list
    # array = []
    # for field in list:
    #     curr = field.currency.code if field.currency else ''
    #     # money = round((field.total, field.subtotal)[int(order_type) == dict(ORDER_TYPE)['SALES ORDER'] or
    #     #                                             int(order_type) == dict(ORDER_TYPE)['PURCHASE ORDER']], 6)
    #     money = OrderItem.objects.filter(is_hidden=0, order_id=field.id) \
    #             .aggregate(total=Sum('amount'))['total']
    #     if field.currency.is_decimal:
    #         separator = intcomma("%.2f" % money)
    #     else:
    #         separator = intcomma("%.0f" % money)
    #     format_money = str(curr + ' ' + separator)

    #     data = {"id": str(field.id),
    #             "update_date": field.update_date.strftime("%d-%m-%Y"),
    #             "document_date": field.document_date.strftime("%d-%m-%Y"),
    #             "document_number": field.document_number,
    #             "reference_number": field.reference_number,
    #             "cust_supp_name": get_cust_supp_name(int(order_type), field),
    #             "total": format_money,
    #             "status": str(field.status)}
    #     array.append(data)

    # content = {"draw": draw, "data": array, "recordsTotal": records_total, "recordsFiltered": records_filtered}
    # json_content = json.dumps(content, ensure_ascii=False)
    # return HttpResponse(json_content, content_type='application/json')

@login_required
def profile_add(request):
    return render(request, 'profile_list.html')

@login_required
def profile_edit(request, profile_id):
    profile = Profile.objects.get(pk=profile_id)
    return render(request, 'profile_list.html')

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