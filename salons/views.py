from django.shortcuts import render
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.urls import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Salon
from django.conf import settings as s
import datetime
import json
from django.contrib import messages
from django.db.models import Q


@csrf_exempt
def get_salon_info(request):
    """
    Method get a salon information.
    """

    context = {
        'salon_name': '',
        'pic_name': '',
        'zip_code': '',
        'address1': '',
        'address2': '',
        'tel': '',
        'prefecture': '',
    }
    if request.method == 'POST':
        try:
            salon_id = request.POST.get('salon_id')
            salon_info = Salon.objects.filter(id=salon_id, is_hidden=False)
            if salon_info:
                salon_info = salon_info.last()
                context = {
                    'name': str(salon_info.name),
                    'pic_name': str(salon_info.pic_name),
                    'zip1': str(salon_info.zip1),
                    'address1': str(salon_info.address1),
                    'address2': str(salon_info.address2),
                    'pic_tel': str(salon_info.pic_tel),
                    'prefecture': str(salon_info.prefecture_id),
                }
        except Exception as e:
            print(e)

    return HttpResponse(json.dumps(context), content_type="application/json")


# @login_required
@csrf_exempt
def update_salon_info(request):
    """
    Method update a salon information.
    """

    message = 'Error'
    if request.method == 'POST':
        try:
            profile_id = request.POST.get('profile_id')
            salon_id = request.POST.get('salon_id')
            name = request.POST.get('name')
            pic_name = request.POST.get('pic_name')
            zip1= request.POST.get('zip_code')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            pic_tel = request.POST.get('pic_tel')
            prefecture = int(request.POST.get('prefecture'))

            if salon_id != '':
                salon_info = Salon.objects.filter(id=salon_id, user_id=profile_id, is_hidden=False)

                if salon_info:
                    salon_info = salon_info.last()
                    salon_info.pic_name = pic_name
                    salon_info.name = name
                    salon_info.address1 = address1
                    salon_info.address2 = address2
                    salon_info.zip1 = zip1
                    salon_info.pic_tel = pic_tel
                    salon_info.prefecture_id = prefecture

                    salon_info.modified = datetime.datetime.now()
                    salon_info.save()
            else:
                salon_info = Salon()
                salon_info.user_id = profile_id
                salon_info.pic_name = pic_name
                salon_info.name = name
                salon_info.address1 = address1
                salon_info.address2 = address2
                salon_info.zip1 = zip1
                salon_info.pic_tel = pic_tel
                salon_info.prefecture_id = prefecture

                salon_info.save()

            message = 'Success'
        except Exception as e:
            print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")


# @login_required
@csrf_exempt
def delete_salon_info(request):
    """
    Method to delete a salon info.
    """

    message = 'Error'
    if request.method == 'POST':
        salon_id = request.POST.get('salon_id')
        try:
            salon = Salon.objects.get(pk=salon_id)
            salon.is_hidden = 1
            salon.modified = datetime.datetime.now()
            salon.save()

            message = 'Success'
        except Exception as e:
            print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")


# @login_required
def SalonList__asJson(request):
    """
    Method to get profile list as JSON.
    """

    draw = request.GET['draw']
    start = request.GET['start']
    length = request.GET['length']
    search = request.GET['search[value]']

    user_id = request.GET.get('user_id')

    salon_list = Salon.objects.filter(user_id=user_id, is_hidden=False).order_by('name')
        
    records_total = salon_list.count()

    if search:  # Filter data base on search
        salon_list = salon_list.filter(Q(name__icontains=search)|Q(pic_name__icontains=search)|Q(pic_tel__icontains=search)).order_by('-name')

    # All data
    records_filtered = salon_list.count()
    # Order by list_limit base on order_dir and order_column
    order_column = request.GET['order[0][column]']
    column_name = ""
    if order_column == "1":
        column_name = "name"
    if order_column == "2":
        column_name = "pic_name"
    if order_column == "4":
        column_name = "pic_tel"
    
    order_dir = request.GET['order[0][dir]']
    list = []
    if order_dir == "asc":
        list = salon_list.order_by(column_name)[int(start):(int(start) + int(length))]
    elif order_dir == "desc":
        list = salon_list.order_by('-' + column_name)[int(start):(int(start) + int(length))]

    array = []
    i = 0
    for field in list:
        i = i + 1
        data = {"no": str(i),
                "id": str(field.id),
                "name": field.name,
                "pic_name": field.pic_name,
                "address": field.address1 + '</br>' + field.address2 + ' Zip:' + field.zip1,
                "pic_tel": field.pic_tel
                }
        array.append(data)

    content = {"draw": draw, "data": array, "recordsTotal": records_total, "recordsFiltered": records_filtered}
    json_content = json.dumps(content, ensure_ascii=False)
    return HttpResponse(json_content, content_type='application/json')