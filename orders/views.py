from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Order, OrderProduct, OrderProductCommission
from products.models import ProductJancode, ProductImage
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
from utilities.common import round_number



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

    filter_str = eval(request.GET.get('filter_str'))
    seller_id = request.GET.get('seller_id')

    order_list = Order.objects.filter(is_hidden=False, seller_id=seller_id).order_by('authority_id')
    if len(filter_str):
        order_list = order_list.filter(status__in=filter_str)
        
    records_total = order_list.count()

    if search:  # Filter data base on search
        order_list = order_list.filter(Q(id__icontains=search)|Q(name__icontains=search)).order_by('-nickname')

    # All data
    records_filtered = order_list.count()
    # Order by list_limit base on order_dir and order_column
    order_column = request.GET['order[0][column]']
    column_name = ""
    if order_column == "0":
        column_name = "id"
    if order_column == "1":
        column_name = "name"
    
    order_dir = request.GET['order[0][dir]']
    list = []
    if order_dir == "asc":
        list = order_list.order_by(column_name)[int(start):(int(start) + int(length))]
    elif order_dir == "desc":
        list = order_list.order_by('-' + column_name)[int(start):(int(start) + int(length))]

    array = []
    for field in list:
        data = {
            "id": str(field.id),
            "name": field.name,
            "address": field.address1 + '  Zip: ' + field.zip1,
            "amount": intcomma("%.0f" % field.total_amount),
            "status": 'IN PROCESSING' if field.status == 1 else 'SHIPMENT COMPLETE',
            "shipped_date": field.shipped_date.strftime("%Y-%m-%d"),
            "inquiry_number": field.inquiry_number
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

    try:
        tax_rate = TaxRate.objects.filter(is_hidden=False, is_enable=True, end_date__isnull=True).last().tax_rate
    except:
        tax_rate = None

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
                        if tax_rate:
                            orderProduct.tax = round_number(orderProduct.total_price * tax_rate, 0)
                        else:
                            orderProduct.tax = 0
                        orderProduct.total_amount = int(orderProduct.total_price + orderProduct.tax)
                        orderProduct.save()

                        product_jan.stock = product_jan.stock - int(item['qty'])
                        product_jan.modified = datetime.datetime.now()
                        product_jan.save()

            return render(request, 'order_list.html')
        except Exception as e:
            print(e)

    orderer_list = list(Profile.objects.filter(is_hidden=False, authority_id__in=[AUTHORITY_TYPE['STORE'], AUTHORITY_TYPE['GENERAL']]).values_list('id', 'nickname', 'authority_id'))
    prefecture_list = list(Prefecture.objects.filter(is_hidden=False, is_enable=True).order_by('id').values_list('id', 'name'))
    return render(request, 'order_form.html', {'prefecture_list': prefecture_list,
                                                'orderer_list': orderer_list,
                                                'order_product_list': [],
                                                'status_list': ORDER_STATUS,
                                                'tax_rate': tax_rate})

# @login_required
def order_edit(request, order_id):
    """
    Method to edit a order.
    """

    try:
        tax_rate = TaxRate.objects.filter(is_hidden=False, is_enable=True, end_date__isnull=True).last().tax_rate
    except:
        tax_rate = None

    if request.method == 'POST':
        try:
            order = Order.objects.get(pk=order_id)
            if order:
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

                # delete old order product
                old_products = OrderProduct.objects.filter(is_hidden=False, order_id=order.id)
                for old_product in old_products:
                    product_jan = ProductJancode.objects.filter(is_hidden=False, id=old_product.product_jan_code_id).first()
                    if product_jan:
                        product_jan.stock = product_jan.stock + old_product.quantity # restore qty
                        product_jan.modified = datetime.datetime.now()
                        product_jan.save()

                    old_product.is_hidden = True
                    old_product.modified = datetime.datetime.now()
                    old_product.save()
                    

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
                            if tax_rate:
                                orderProduct.tax = round_number(orderProduct.total_price * tax_rate, 0)
                            else:
                                orderProduct.tax = 0
                            orderProduct.total_amount = int(orderProduct.total_price + orderProduct.tax)
                            orderProduct.save()

                            product_jan.stock = product_jan.stock - int(item['qty'])
                            product_jan.modified = datetime.datetime.now()
                            product_jan.save()

            return render(request, 'order_list.html')

        except Exception as e:
            print(e)

    order = Order.objects.get(pk=order_id)

    order_products = OrderProduct.objects.filter(is_hidden=False, order_id=order.id)
    order_product_list = []
    for order_product in order_products:
        product_jan = ProductJancode.objects.filter(pk=order_product.product_jan_code_id).first()
        # # product
        # j_product = get_jan_products(product_jan)
        # # image
        # p_image = ProductImage.objects.filter(
        #                 product_id=j_product.id, is_hidden=False).order_by('image_no').exclude(image_no__isnull=True).first()
        # if p_image:
        #     image_path = p_image.image.image.url
        # else:
        #     image_path = ''

        # order_product_list.append([order_product.product_jan_code_id, order_product.quantity, image_path])
        order_product_list.append([order_product.product_jan_code_id, order_product.quantity])

    orderer_list = list(Profile.objects.filter(is_hidden=False, authority_id__in=[AUTHORITY_TYPE['STORE'], AUTHORITY_TYPE['GENERAL']]).values_list('id', 'nickname', 'authority_id'))
    prefecture_list = list(Prefecture.objects.filter(is_hidden=False, is_enable=True).order_by('id').values_list('id', 'name'))
    
    return render(request, 'order_form.html', {'prefecture_list': prefecture_list,
                                                'order': order,
                                                'orderer_list': orderer_list,
                                                'order_product_list': order_product_list,
                                                'status_list': ORDER_STATUS,
                                                'tax_rate': tax_rate})

# @login_required
@csrf_exempt
def order_delete(request, order_id):
    """
    Method to delete a order.
    """

    try:
        order = Order.objects.get(pk=order_id)
        order.is_hidden = True
        order.modified = datetime.datetime.now()
        order.save()

        # delete old order product
        old_products = OrderProduct.objects.filter(is_hidden=False, order_id=order.id)
        for old_product in old_products:
            product_jan = ProductJancode.objects.filter(is_hidden=False, id=old_product.product_jan_code_id).first()
            if product_jan:
                product_jan.stock = product_jan.stock + old_product.quantity # restore qty
                product_jan.modified = datetime.datetime.now()
                product_jan.save()
            
            old_product.is_hidden = True
            old_product.modified = datetime.datetime.now()
            old_product.save()

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