from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.urls import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Product
from prefectures.models import Prefecture
from images.models import Image
from django.conf import settings as s
import datetime
import json
from django.contrib import messages
from django.db.models import Q



# @login_required
def product_list(request):
    """
    Method to redirect to product list page.
    """

    return render(request, 'product_list.html')

# @login_required
def ProductList__asJson(request):
    """
    Method to get product list as JSON.
    """

    draw = request.GET['draw']
    start = request.GET['start']
    length = request.GET['length']
    search = request.GET['search[value]']

    auth_type = eval(request.GET.get('filter_str'))

    product_list = Product.objects.filter(authority_id__in=auth_type, is_hidden=False).order_by('authority_id')
    if 0 in auth_type:
        product_list = product_list.filter(is_approved=False)
        
    records_total = product_list.count()

    if search:  # Filter data base on search
        product_list = product_list.filter(Q(nickname__icontains=search)).order_by('-nickname')

    # All data
    records_filtered = product_list.count()
    # Order by list_limit base on order_dir and order_column
    order_column = request.GET['order[0][column]']
    column_name = ""
    if order_column == "2":
        column_name = "nickname"
    
    order_dir = request.GET['order[0][dir]']
    list = []
    if order_dir == "asc":
        list = product_list.order_by(column_name)[int(start):(int(start) + int(length))]
    elif order_dir == "desc":
        list = product_list.order_by('-' + column_name)[int(start):(int(start) + int(length))]

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
def product_add(request):
    """
    Method to add new product.
    """
    form = None
    # if request.method == 'POST':
    #     form = ProfileForm(request.POST)

    # else:
    #     form = ProfileForm()
    return render(request, 'product_form.html', {'form': form, 
                                                'media_url': s.MEDIA_URL})

# @login_required
def product_edit(request, product_id):
    """
    Method to edit a product.
    """

    form = None
    return render(request, 'product_form.html', {'form': form, 
                                                'media_url': s.MEDIA_URL})

# @login_required
@csrf_exempt
def product_delete(request, product_id):
    """
    Method to delete a product.
    """

    try:
        product = Product.objects.get(pk=product_id)
        product.is_hidden = 1
        product.modified = datetime.datetime.now()
        product.save()
    except Exception as e:
        print(e)
    return render(request, 'product_list.html')