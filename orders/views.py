from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderProduct, OrderProductCommission
from prefectures.models import Prefecture
from profiles.models import Profile
from django.conf import settings as s
import datetime
import json
from django.contrib import messages
from django.db.models import Q
from utilities.constants import AUTHORITY_TYPE, ORDER_STATUS



# @login_required
def order_list(request):
    """
    Method to redirect to order list page.
    """

    return render(request, 'order_list.html')

# @login_required
def OrderList__asJson(request):
    """
    Method to get order list as JSON.
    """

    draw = request.GET['draw']
    start = request.GET['start']
    length = request.GET['length']
    search = request.GET['search[value]']

    auth_type = eval(request.GET.get('filter_str'))

    order_list = Order.objects.filter(authority_id__in=auth_type, is_hidden=False).order_by('authority_id')
    if 0 in auth_type:
        order_list = order_list.filter(is_approved=False)
        
    records_total = order_list.count()

    if search:  # Filter data base on search
        order_list = order_list.filter(Q(nickname__icontains=search)).order_by('-nickname')

    # All data
    records_filtered = order_list.count()
    # Order by list_limit base on order_dir and order_column
    order_column = request.GET['order[0][column]']
    column_name = ""
    if order_column == "2":
        column_name = "nickname"
    
    order_dir = request.GET['order[0][dir]']
    list = []
    if order_dir == "asc":
        list = order_list.order_by(column_name)[int(start):(int(start) + int(length))]
    elif order_dir == "desc":
        list = order_list.order_by('-' + column_name)[int(start):(int(start) + int(length))]

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
def order_add(request):
    """
    Method to add new order.
    """

    orderer_list = list(Profile.objects.filter(is_hidden=False, authority_id__in=[AUTHORITY_TYPE['STORE'], AUTHORITY_TYPE['GENERAL']]).values_list('id', 'nickname'))
    prefecture_list = list(Prefecture.objects.filter(is_hidden=False, is_enable=True).order_by('id').values_list('id', 'name'))
    return render(request, 'order_form.html', {'prefecture_list': prefecture_list,
                                                'orderer_list': orderer_list,
                                                'status_list': ORDER_STATUS})

# @login_required
def order_edit(request, order_id):
    """
    Method to edit a order.
    """

    try:
        order = Order.objects.get(pk=order_id)
    except Exception as e:
        print(e)

    orderer_list = list(Profile.objects.filter(is_hidden=False, authority_id__in=[AUTHORITY_TYPE['STORE'], AUTHORITY_TYPE['GENERAL']]).values_list('id', 'nickname'))
    prefecture_list = list(Prefecture.objects.filter(is_hidden=False, is_enable=True).order_by('id').values_list('id', 'name'))
    return render(request, 'order_form.html', {'prefecture_list': prefecture_list,
                                                'order': order,
                                                'orderer_list': orderer_list,
                                                'status_list': ORDER_STATUS})

# @login_required
@csrf_exempt
def order_delete(request, order_id):
    """
    Method to delete a order.
    """

    try:
        order = Order.objects.get(pk=order_id)
        order.is_hidden = 1
        order.modified = datetime.datetime.now()
        order.save()
    except Exception as e:
        print(e)
    return render(request, 'order_list.html')
