from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Order, OrderProduct, OrderProductCommission
from products.models import ProductJancode
from products.views import get_jan_products
from prefectures.models import Prefecture
from profiles.models import Profile
from taxes.models import TaxRate
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
    if request.method == 'POST':
        try:
            order = Order()
            order.seller_id = request.POST.get('seller_id')
            order.purchaser_id = request.POST.get('orderer')
            order.amount = request.POST.get('amount')
            order.tax = request.POST.get('tax')
            order.shipping_fee = request.POST.get('shipping_fee')
            order.total_amount = request.POST.get('total_amount')
            order.name = request.POST.get('name')
            order.zip1 = request.POST.get('zip1')
            order.prefecture_id = request.POST.get('prefecture')
            order.address1 = request.POST.get('address1')
            order.address2 = request.POST.get('address2')
            order.tel = request.POST.get('tel')
            order.status = request.POST.get('order_status')
            order.inquiry_number = request.POST.get('inquiry_number')
            order.order_date = request.POST.get('order_date')
            order.shipped_date = request.POST.get('shipped_date')
            order.save()

            product_list = json.loads(request.POST.get('product_list'))
            for item in product_list:
                product_jan = ProductJancode.objects.filter(pk=item['jan_id']).first()
                if (product_jan):
                    j_product = get_jan_products(product_jan)
                    if j_product:
                        orderProduct = OrderProduct()
                        orderProduct.product_jan_code_id = item['jan_id']
                        orderProduct.order_id = order.id
                        orderProduct.quantity = item['qty']
                        orderProduct.unit_price = j_product.price
                        orderProduct.total_price = int(j_product.price) * int(item['qty'])
                        # orderProduct.tax = 
                        orderProduct.total_amount = int(orderProduct.total_price + orderProduct.tax)
                        orderProduct.save()

        except:
            pass


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


def check_for_duplicate(request, type, value):
    """
    Method to verify duplcate info.
    """

    message = 'Error'
    try:
        order = None
        if type == 'inquiry_number':
            order = Order.objects.filter(inquiry_number=value).first()
        # elif type == '':
        #     product = Product.objects.filter(user_code=value).first()

        if order:
            message = 'Success'
    except Exception as e:
        print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")