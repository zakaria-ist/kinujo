import datetime
import json
import threading
from django.contrib import messages
from django.db.models import Q, Sum, Value
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import Order, OrderProduct, OrderProductCommission, TotalCommission, TotalSale
from products.models import ProductJancode, ProductImage
from products.views import get_jan_products
from prefectures.models import Prefecture
from profiles.models import Profile, Authority, UserSale, UserCommision
from taxes.models import TaxRate
from utilities.constants import AUTHORITY_TYPE, ORDER_STATUS
from utilities.common import round_number



@login_required
def order_list(request):
    """
    Method to redirect to order list page.
    """

    if request.session['login_type'] == 'SELLER':
        return render(request, 'order_list.html')
    else:
        return render(request, '404.html')


@login_required
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
    if not seller_id:
        seller_id = request.session['login_profile_id']

    order_list = Order.objects.filter(is_hidden=False, seller_id=seller_id).order_by('authority_id')
    if len(filter_str):
        order_list = order_list.filter(status__in=filter_str)
        
    records_total = order_list.count()

    if search:  # Filter data base on search
        order_list = order_list.filter(Q(id__icontains=search)|Q(name__icontains=search)).order_by('-name')

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


def if_kinujo_product(seller_id):
    """
    Method to define the product owner is Kinujo or not.
    """

    kinujo_product = True
    try:
        if seller_id:
            seller_authority = Profile.objects.get(pk=seller_id).authority_id
            if seller_authority != AUTHORITY_TYPE['MASTER']:
                kinujo_product = False
    except Exception as e:
        print('if_kinujo_product', e)

    return kinujo_product


def get_commission(introducer, kinujo_product):
    """
    Method to get commission rate.
    """

    commission = 0
    authorities = Authority.objects.filter(is_hidden = False)
    if kinujo_product:
        commission = authorities.filter(pk=introducer.authority_id).first().official_commission_rate
    else:
        commission = authorities.filter(pk=introducer.authority_id).first().commission_rate

    return commission


def get_commission_holder_list(buyer_id, kinujo_product):
    """
    Method to create commission holder list.
    """

    commission_holder_list = []
    try:
        if buyer_id:
            buyer = Profile.objects.get(pk=buyer_id)
            if buyer.introducer_id and \
                    buyer.introducer.authority_id != AUTHORITY_TYPE['MASTER']:
                buyer_introducer = Profile.objects.filter(pk=buyer.introducer_id).first()
                if buyer_introducer:
                    commission = get_commission(buyer_introducer, kinujo_product)
                    commission_holder_list.append({
                        "user_id": buyer_introducer.id,
                        "auth_id": buyer_introducer.authority_id,
                        "commission": commission
                    })

                    if buyer_introducer.introducer_id and \
                            buyer_introducer.introducer.authority_id != AUTHORITY_TYPE['MASTER']:
                        buyer_introducer_introducer = Profile.objects.filter(pk=buyer_introducer.introducer_id).first()
                        if buyer_introducer_introducer:
                            commission = get_commission(buyer_introducer_introducer, kinujo_product)
                            commission_holder_list.append({
                                "user_id": buyer_introducer_introducer.id,
                                "auth_id": buyer_introducer_introducer.authority_id,
                                "commission": commission
                            })

                            if buyer_introducer_introducer.introducer_id and \
                                    buyer_introducer_introducer.introducer.authority_id != AUTHORITY_TYPE['MASTER']:
                                buyer_introducer_introducer_introducer = Profile.objects.filter(pk=buyer_introducer_introducer.introducer_id).first()
                                if buyer_introducer_introducer_introducer:
                                    commission = get_commission(buyer_introducer_introducer_introducer, kinujo_product)
                                    commission_holder_list.append({
                                        "user_id": buyer_introducer_introducer_introducer.id,
                                        "auth_id": buyer_introducer_introducer_introducer.authority_id,
                                        "commission": commission
                                    })

                                    if buyer_introducer_introducer_introducer.introducer_id and \
                                            buyer_introducer_introducer_introducer.introducer.authority_id != AUTHORITY_TYPE['MASTER']:
                                        buyer_introducer_introducer_introducer_introducer = Profile.objects.filter(pk=buyer_introducer_introducer_introducer.introducer_id).first()
                                        if buyer_introducer_introducer_introducer_introducer:
                                            commission = get_commission(buyer_introducer_introducer_introducer_introducer, kinujo_product)
                                            commission_holder_list.append({
                                                "user_id": buyer_introducer_introducer_introducer_introducer.id,
                                                "auth_id": buyer_introducer_introducer_introducer_introducer.authority_id,
                                                "commission": commission
                                            })
    except Exception as e:
        print('get_commission_holder_list', e)

    return commission_holder_list


def update_monthly_commission_data(affected_user_list, order_date):
    """
    Method to update monthly user sales & commission.
    """

    try:
        tax_rate = TaxRate.objects.filter(is_hidden=False, is_enable=True, end_date__isnull=True).last().tax_rate
    except:
        tax_rate = None
    try:
        year = order_date.year
        month = order_date.month
        for user in affected_user_list:
            user_commission_data = OrderProductCommission.objects.filter(user_id=user,
                                    is_hidden=False, 
                                    order_product__is_hidden=False,
                                    order_product__order__is_hidden=False,
                                    order_product__order__order_date__month=month,
                                    order_product__order__order_date__year=year)
            
            user_sales_count = user_commission_data.filter(is_sales=True).count()
            user_sales_total = user_commission_data.filter(is_sales=True)\
                    .aggregate(sales_amount=Coalesce(Sum('amount'), Value(0)), 
                                shipping=Coalesce(Sum('shipping_fee'), Value(0)))
            user_commission_count = user_commission_data.filter(is_sales=False).count()
            user_commission_total = user_commission_data.filter(is_sales=False)\
                    .aggregate(com_amount=Coalesce(Sum('amount'), Value(0)))

            # update user sales
            user_sale = UserSale.objects.filter(is_hidden=False, user_id=user,
                                    year=year, month=month)
            if user_sale:
                user_sale = user_sale.first()
            else:
                user_sale = UserSale()
            user_sale.year = year
            user_sale.month = month
            user_sale.user_id = user
            user_sale.order_count = user_sales_count
            user_sale.sales_amount = user_sales_total.get('sales_amount', 0)
            if tax_rate:
                user_sale.tax = user_sale.sales_amount * tax_rate
            else:
                user_sale.tax = 0
            user_sale.amount_tax_included = user_sale.sales_amount + user_sale.tax
            user_sale.shipping_fee = user_sales_total.get('shipping', 0)
            user_sale.total_amount = user_sale.amount_tax_included + user_sale.shipping_fee
            user_sale.modified = datetime.datetime.now()
            user_sale.save()

            # update user sales
            user_commission = UserCommision.objects.filter(is_hidden=False, user_id=user,
                                    year=year, month=month)
            if user_commission:
                user_commission = user_commission.first()
            else:
                user_commission = UserCommision()
            user_commission.year = year
            user_commission.month = month
            user_commission.user_id = user
            user_commission.order_count = user_commission_count
            user_commission.amount = user_commission_total.get('com_amount', 0)
            if tax_rate:
                user_commission.tax = user_commission.amount * tax_rate
            else:
                user_commission.tax = 0
            user_commission.total_amount = user_commission.amount + user_commission.tax
            user_commission.modified = datetime.datetime.now()
            user_commission.save()
        
        # update total sales
        total_sales_total = UserSale.objects.filter(is_hidden=False, year=year, month=month)\
                    .aggregate(total_sales_amount=Coalesce(Sum('sales_amount'), Value(0)), 
                                total_tax=Coalesce(Sum('tax'), Value(0)),
                                total_amount_tax_included=Coalesce(Sum('amount_tax_included'), Value(0)),
                                total_shipping_fee=Coalesce(Sum('shipping_fee'), Value(0)),
                                total_total_amount=Coalesce(Sum('total_amount'), Value(0)),
                                total_order_count=Coalesce(Sum('order_count'), Value(0)))
                    
        total_sales = TotalSale.objects.filter(is_hidden=False, year=year, month=month)
        if total_sales:
            total_sales = total_sales.first()
        else:
            total_sales = TotalSale()
        total_sales.year = year
        total_sales.month = month
        total_sales.sales_amount = total_sales_total.get('total_sales_amount', 0)
        total_sales.tax = total_sales_total.get('total_tax', 0)
        total_sales.amount_tax_included = total_sales_total.get('total_amount_tax_included', 0)
        total_sales.shipping_fee = total_sales_total.get('total_shipping_fee', 0)
        total_sales.total_amount = total_sales_total.get('total_total_amount', 0)
        total_sales.order_count = total_sales_total.get('total_order_count', 0)
        total_sales.modified = datetime.datetime.now()
        total_sales.save()

        # update total commission
        authorities = list(Authority.objects.filter(is_hidden = False).values_list('id', flat=True))
        for auth_id in authorities:
            total_commission_total = UserCommision.objects.filter(is_hidden=False, year=year, month=month, user__authority_id=auth_id)\
                        .aggregate(total_com_amount=Coalesce(Sum('amount'), Value(0)),
                                    total_order_count=Coalesce(Sum('order_count'), Value(0)))

            total_commissions = TotalCommission.objects.filter(is_hidden=False, year=year, month=month, authority_id=auth_id)
            if total_commissions:
                total_commissions = total_commissions.first()
            else:
                total_commissions = TotalCommission()
            total_commissions.year = year
            total_commissions.month = month
            total_commissions.authority_id = auth_id
            total_commissions.amount = total_commission_total.get('total_com_amount', 0)
            total_commissions.order_count = total_commission_total.get('total_order_count', 0)
            total_commissions.modified = datetime.datetime.now()
            total_commissions.save()

    except Exception as e:
        print('update_monthly_commission_data', e)


@login_required
def order_add(request):
    """
    Method to add new order.
    """

    if request.session['login_type'] == 'SELLER':
        try:
            tax_rate = TaxRate.objects.filter(is_hidden=False, is_enable=True, end_date__isnull=True).last().tax_rate
        except:
            tax_rate = None

        seller_id = request.session['login_profile_id']
        if request.method == 'POST':
            try:
                order = Order()
                order.seller_id = seller_id
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
                kinujo_product = if_kinujo_product(order.seller_id)
                commission_holder_list = get_commission_holder_list(order.purchaser_id, kinujo_product)
                orderer_auth_type = Profile.objects.get(pk=order.purchaser_id).authority_id
                
                affected_user_list = []
                for item in product_list:
                    product_jan = ProductJancode.objects.filter(pk=item['jan_id']).first()
                    if (product_jan):
                        j_product = get_jan_products(product_jan)
                        if j_product:
                            orderProduct = OrderProduct()
                            orderProduct.product_jan_code_id = item['jan_id']
                            orderProduct.order_id = order.id
                            orderProduct.quantity = item['qty']
                            if orderer_auth_type == AUTHORITY_TYPE['STORE']:
                                orderProduct.unit_price = j_product.store_price
                            else:
                                orderProduct.unit_price = j_product.price
                            orderProduct.total_price = int(orderProduct.unit_price) * int(item['qty'])
                            if tax_rate:
                                orderProduct.tax = round_number(orderProduct.total_price * tax_rate, 0)
                            else:
                                orderProduct.tax = 0
                            orderProduct.total_amount = orderProduct.total_price + orderProduct.tax
                            orderProduct.save()

                            product_jan.stock = product_jan.stock - int(item['qty'])
                            product_jan.modified = datetime.datetime.now()
                            product_jan.save()

                            # commissoion block
                            if kinujo_product:
                                remaining_amount = int(j_product.price) * int(orderProduct.quantity)
                                if orderer_auth_type == AUTHORITY_TYPE['STORE']:
                                    remaining_amount = int(j_product.store_price) * int(orderProduct.quantity)
                                # others commission
                                for commission_holder in commission_holder_list:
                                    if float(commission_holder['commission']) != 0:
                                        his_amount = int(j_product.price  * int(orderProduct.quantity) * float(commission_holder['commission']))
                                        remaining_amount = remaining_amount - his_amount
                                        orderProductCommission = OrderProductCommission()
                                        orderProductCommission.order_product_id = orderProduct.id
                                        orderProductCommission.user_id = commission_holder['user_id']
                                        orderProductCommission.amount = his_amount
                                        orderProductCommission.is_sales = False
                                        orderProductCommission.is_food = False
                                        orderProductCommission.shipping_fee = 0
                                        orderProductCommission.save()
                                        if orderProductCommission.user_id not in affected_user_list:
                                            affected_user_list.append(orderProductCommission.user_id)
                                    # elif float(commission_holder['commission']) == 0:
                                    #     his_amount = remaining_amount
                                    #     remaining_amount = remaining_amount - his_amount
                                    #     orderProductCommission = OrderProductCommission()
                                    #     orderProductCommission.order_product_id = orderProduct.id
                                    #     orderProductCommission.user_id = commission_holder['user_id']
                                    #     orderProductCommission.amount = his_amount
                                    #     orderProductCommission.is_sales = False
                                    #     orderProductCommission.is_food = False
                                    #     orderProductCommission.shipping_fee = 0
                                    #     orderProductCommission.save()
                                    #     if orderProductCommission.user_id not in affected_user_list:
                                            # affected_user_list.append(orderProductCommission.user_id)
                                # create master seller commission
                                if remaining_amount > 0:
                                    orderProductCommission = OrderProductCommission()
                                    orderProductCommission.order_product_id = orderProduct.id
                                    orderProductCommission.user_id = order.seller_id
                                    orderProductCommission.amount = remaining_amount
                                    orderProductCommission.is_sales = True
                                    orderProductCommission.is_food = False
                                    orderProductCommission.shipping_fee = j_product.shipping_fee
                                    orderProductCommission.save()
                                    if orderProductCommission.user_id not in affected_user_list:
                                        affected_user_list.append(orderProductCommission.user_id)
                            
                            else: # Non Kinujo Products
                                seller_commission = 0.65
                                seller_amount = int(j_product.price * seller_commission) * int(orderProduct.quantity)
                                remaining_amount = int(j_product.price) * int(orderProduct.quantity)
                                if orderer_auth_type == AUTHORITY_TYPE['STORE']:
                                    remaining_amount = int(j_product.store_price) * int(orderProduct.quantity)
                                remaining_amount = remaining_amount - seller_amount
                                # create seller commission
                                orderProductCommission = OrderProductCommission()
                                orderProductCommission.order_product_id = orderProduct.id
                                orderProductCommission.user_id = order.seller_id
                                orderProductCommission.amount = seller_amount
                                orderProductCommission.is_sales = True
                                orderProductCommission.is_food = False
                                orderProductCommission.shipping_fee = j_product.shipping_fee
                                orderProductCommission.save()
                                if orderProductCommission.user_id not in affected_user_list:
                                    affected_user_list.append(orderProductCommission.user_id)
                                # now others commission
                                for commission_holder in commission_holder_list:
                                    if float(commission_holder['commission']) != 0:
                                        his_amount = int(j_product.price  * int(orderProduct.quantity) * float(commission_holder['commission']))
                                        remaining_amount = remaining_amount - his_amount
                                        orderProductCommission = OrderProductCommission()
                                        orderProductCommission.order_product_id = orderProduct.id
                                        orderProductCommission.user_id = commission_holder['user_id']
                                        orderProductCommission.amount = his_amount
                                        orderProductCommission.is_sales = False
                                        orderProductCommission.is_food = False
                                        orderProductCommission.shipping_fee = 0
                                        orderProductCommission.save()
                                        if orderProductCommission.user_id not in affected_user_list:
                                            affected_user_list.append(orderProductCommission.user_id)
                                if remaining_amount > 0:
                                    last_user = Profile.objects.filter(is_hidden=False, is_master=True, 
                                            authority_id=AUTHORITY_TYPE['MASTER']).first()
                                    if last_user:
                                        orderProductCommission = OrderProductCommission()
                                        orderProductCommission.order_product_id = orderProduct.id
                                        orderProductCommission.user_id = last_user.id
                                        orderProductCommission.amount = remaining_amount
                                        orderProductCommission.is_sales = False
                                        orderProductCommission.is_food = False
                                        orderProductCommission.shipping_fee = 0
                                        orderProductCommission.save()
                                        if orderProductCommission.user_id not in affected_user_list:
                                            affected_user_list.append(orderProductCommission.user_id)
                            


                # Update users monthly commission & total commission
                update_users_monthly_commission_t = threading.Thread(name='update_monthly_commission_t',
                                                            target=update_monthly_commission_data, 
                                                            args=(affected_user_list, order.order_date,  ), daemon=True)
                update_users_monthly_commission_t.start()

                return render(request, 'order_list.html')
            except Exception as e:
                print(e)

        orderer_list = list(Profile.objects.filter(is_hidden=False, 
                    authority_id__in=[AUTHORITY_TYPE['STORE'], AUTHORITY_TYPE['GENERAL']])\
            .exclude(id=seller_id)\
            .values_list('id', 'real_name', 'authority_id'))
        prefecture_list = list(Prefecture.objects.filter(is_hidden=False, is_enable=True).order_by('id').values_list('id', 'name'))
        return render(request, 'order_form.html', {'prefecture_list': prefecture_list,
                                                    'orderer_list': orderer_list,
                                                    'order_product_list': [],
                                                    'status_list': ORDER_STATUS,
                                                    'tax_rate': tax_rate,
                                                    'seller_id': seller_id})
    else:
        return render(request, '404.html')

@login_required
def order_edit(request, order_id):
    """
    Method to edit a order.
    """

    if request.session['login_type'] == 'SELLER':
        try:
            tax_rate = TaxRate.objects.filter(is_hidden=False, is_enable=True, end_date__isnull=True).last().tax_rate
        except:
            tax_rate = None

        seller_id = request.session['login_profile_id']
        if request.method == 'POST':
            try:
                order = Order.objects.filter(pk=order_id, seller_id=seller_id)
                if order.exists():
                    order = order.first()
                    # order.seller_id = request.POST.get('seller_id')
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

                    affected_user_list = []
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

                        # delete old orderproduct commission
                        orderProductCommissions = OrderProductCommission.object.filter(order_product_id=old_product.id)
                        for orderProductCommission in orderProductCommissions:
                            orderProductCommission.is_hidden = True
                            orderProductCommission.save()

                            if orderProductCommission.user_id not in affected_user_list:
                                affected_user_list.append(orderProductCommission.user_id)

                        

                    product_list = json.loads(request.POST.get('product_list'))
                    kinujo_product = if_kinujo_product(order.seller_id)
                    commission_holder_list = get_commission_holder_list(order.purchaser_id, kinujo_product)
                    orderer_auth_type = Profile.objects.get(pk=order.purchaser_id).authority_id

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
                            
                                # commissoion block
                                if kinujo_product:
                                    remaining_amount = int(j_product.price) * int(orderProduct.quantity)
                                    if orderer_auth_type == AUTHORITY_TYPE['STORE']:
                                        remaining_amount = int(j_product.store_price) * int(orderProduct.quantity)
                                    # others commission
                                    for commission_holder in commission_holder_list:
                                        if float(commission_holder['commission']) != 0:
                                            his_amount = int(j_product.price  * int(orderProduct.quantity) * float(commission_holder['commission']))
                                            remaining_amount = remaining_amount - his_amount
                                            orderProductCommission = OrderProductCommission()
                                            orderProductCommission.order_product_id = orderProduct.id
                                            orderProductCommission.user_id = commission_holder['user_id']
                                            orderProductCommission.amount = his_amount
                                            orderProductCommission.is_sales = False
                                            orderProductCommission.is_food = False
                                            orderProductCommission.shipping_fee = 0
                                            orderProductCommission.save()
                                            if orderProductCommission.user_id not in affected_user_list:
                                                affected_user_list.append(orderProductCommission.user_id)
                                        
                                    # create master seller commission
                                    if remaining_amount > 0:
                                        orderProductCommission = OrderProductCommission()
                                        orderProductCommission.order_product_id = orderProduct.id
                                        orderProductCommission.user_id = order.seller_id
                                        orderProductCommission.amount = remaining_amount
                                        orderProductCommission.is_sales = True
                                        orderProductCommission.is_food = False
                                        orderProductCommission.shipping_fee = j_product.shipping_fee
                                        orderProductCommission.save()
                                        if orderProductCommission.user_id not in affected_user_list:
                                            affected_user_list.append(orderProductCommission.user_id)
                                
                                else: # Non Kinujo Products
                                    seller_commission = 0.65
                                    seller_amount = int(j_product.price * seller_commission) * int(orderProduct.quantity)
                                    remaining_amount = int(j_product.price) * int(orderProduct.quantity)
                                    if orderer_auth_type == AUTHORITY_TYPE['STORE']:
                                        remaining_amount = int(j_product.store_price) * int(orderProduct.quantity)
                                    remaining_amount = remaining_amount - seller_amount
                                    # create seller commission
                                    orderProductCommission = OrderProductCommission()
                                    orderProductCommission.order_product_id = orderProduct.id
                                    orderProductCommission.user_id = order.seller_id
                                    orderProductCommission.amount = seller_amount
                                    orderProductCommission.is_sales = True
                                    orderProductCommission.is_food = False
                                    orderProductCommission.shipping_fee = j_product.shipping_fee
                                    orderProductCommission.save()
                                    if orderProductCommission.user_id not in affected_user_list:
                                        affected_user_list.append(orderProductCommission.user_id)
                                    # now others commission
                                    for commission_holder in commission_holder_list:
                                        if float(commission_holder['commission']) != 0:
                                            his_amount = int(j_product.price  * int(orderProduct.quantity) * float(commission_holder['commission']))
                                            remaining_amount = remaining_amount - his_amount
                                            orderProductCommission = OrderProductCommission()
                                            orderProductCommission.order_product_id = orderProduct.id
                                            orderProductCommission.user_id = commission_holder['user_id']
                                            orderProductCommission.amount = his_amount
                                            orderProductCommission.is_sales = False
                                            orderProductCommission.is_food = False
                                            orderProductCommission.shipping_fee = 0
                                            orderProductCommission.save()
                                            if orderProductCommission.user_id not in affected_user_list:
                                                affected_user_list.append(orderProductCommission.user_id)
                                    if remaining_amount > 0:
                                        last_user = Profile.objects.filter(is_hidden=False, is_master=True, 
                                                authority_id=AUTHORITY_TYPE['MASTER']).first()
                                        if last_user:
                                            orderProductCommission = OrderProductCommission()
                                            orderProductCommission.order_product_id = orderProduct.id
                                            orderProductCommission.user_id = last_user.id
                                            orderProductCommission.amount = remaining_amount
                                            orderProductCommission.is_sales = False
                                            orderProductCommission.is_food = False
                                            orderProductCommission.shipping_fee = 0
                                            orderProductCommission.save()
                                            if orderProductCommission.user_id not in affected_user_list:
                                                affected_user_list.append(orderProductCommission.user_id)
                                


                    # Update users monthly commission & total commission
                    update_users_monthly_commission_te = threading.Thread(name='update_monthly_commission_te',
                                                                target=update_monthly_commission_data, 
                                                                args=(affected_user_list, order.order_date,  ), daemon=True)
                    update_users_monthly_commission_te.start()

                return render(request, 'order_list.html')

            except Exception as e:
                print(e)

        order = Order.objects.filter(pk=order_id, seller_id=seller_id)
        if order.exists():
            order = order.first()

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

            orderer_list = list(Profile.objects.filter(is_hidden=False, 
                        authority_id__in=[AUTHORITY_TYPE['STORE'], AUTHORITY_TYPE['GENERAL']])\
                .exclude(id=seller_id)\
                .values_list('id', 'real_name', 'authority_id'))
            prefecture_list = list(Prefecture.objects.filter(is_hidden=False, is_enable=True).order_by('id').values_list('id', 'name'))
            return render(request, 'order_form.html', {'prefecture_list': prefecture_list,
                                                        'order': order,
                                                        'orderer_list': orderer_list,
                                                        'order_product_list': order_product_list,
                                                        'status_list': ORDER_STATUS,
                                                        'tax_rate': tax_rate,
                                                        'seller_id': seller_id})
        else:
            return render(request, '404.html')
    else:
        return render(request, '404.html')

@login_required
# @csrf_exempt
def order_delete(request, order_id):
    """
    Method to delete a order.
    """

    if request.session['login_type'] == 'SELLER':
        try:
            order = Order.objects.get(pk=order_id)
            order.is_hidden = True
            order.modified = datetime.datetime.now()
            order.save()

            # delete old order product
            affected_user_list = []
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

                # delete old orderproduct commission
                orderProductCommissions = OrderProductCommission.object.filter(order_product_id=old_product.id)
                for orderProductCommission in orderProductCommissions:
                    orderProductCommission.is_hidden = True
                    orderProductCommission.save()

                    if orderProductCommission.user_id not in affected_user_list:
                        affected_user_list.append(orderProductCommission.user_id)

            # Update users monthly commission & total commission
            update_users_monthly_commission_td = threading.Thread(name='update_monthly_commission_td',
                                                        target=update_monthly_commission_data, 
                                                        args=(affected_user_list, order.order_date,  ), daemon=True)
            update_users_monthly_commission_td.start()

        except Exception as e:
            print(e)
        return render(request, 'order_list.html')

    else:
        return render(request, '404.html')


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


# @login_required
def UserSalesList__asJson(request):
    """
    Method to get user product sales list as JSON.
    """

    draw = request.GET['draw']
    start = request.GET['start']
    length = request.GET['length']
    # search = request.GET['search[value]']

    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    profile_id = request.session['login_profile_id']
    auth_type = request.session['login_authority_id']

    if auth_type == AUTHORITY_TYPE['MASTER']:
        sales_list = OrderProductCommission.objects.filter(is_hidden=False,
                                user__authority_id=auth_type, is_sales=True,
                                order_product__order__order_date__year=year,
                                order_product__order__order_date__month=month,).order_by('order_product__order__order_date')
    else:
        sales_list = OrderProductCommission.objects.filter(is_hidden=False,
                                user_id=profile_id, is_sales=True,
                                order_product__order__order_date__year=year,
                                order_product__order__order_date__month=month,).order_by('order_product__order__order_date')
        

    array = []
    for field in sales_list:
        product_jan = ProductJancode.objects.filter(pk=field.order_product.id).first()
        if (product_jan):
            j_product = get_jan_products(product_jan)
            productImage = ProductImage.objects.filter(product_id=j_product.id, is_hidden=False)\
                .order_by('image_no').exclude(image_no__isnull=True).first()
            image_path = ''
            if productImage:
                image_path = productImage.image.image.url
            data = {
                "id": str(field.id),
                "date": field.order_product.order.order_date.strftime("%Y-%m-%d"),
                "image_path": image_path,
                "name": j_product.name,
                "amount": field.amount
            }
            array.append(data)

    records_total = len(array)
    records_filtered = len(array)
    content = {"draw": draw, "data": array, "recordsTotal": records_total, "recordsFiltered": records_filtered}
    json_content = json.dumps(content, ensure_ascii=False)
    return HttpResponse(json_content, content_type='application/json')


# @login_required
def UserCommissionList__asJson(request):
    """
    Method to get user product commission list as JSON.
    """

    draw = request.GET['draw']
    start = request.GET['start']
    length = request.GET['length']
    # search = request.GET['search[value]']

    year = int(request.GET.get('year'))
    month = int(request.GET.get('month'))
    profile_id = request.session['login_profile_id']
    auth_type = request.session['login_authority_id']

    if auth_type == AUTHORITY_TYPE['MASTER']:
        sales_list = OrderProductCommission.objects.filter(is_hidden=False,
                                user__authority_id=auth_type, is_sales=False,
                                order_product__order__order_date__year=year,
                                order_product__order__order_date__month=month,).order_by('order_product__order__order_date')
    else:
        sales_list = OrderProductCommission.objects.filter(is_hidden=False,
                                user_id=profile_id, is_sales=False,
                                order_product__order__order_date__year=year,
                                order_product__order__order_date__month=month,).order_by('order_product__order__order_date')
        

    array = []
    for field in sales_list:
        product_jan = ProductJancode.objects.filter(pk=field.order_product.id).first()
        if (product_jan):
            j_product = get_jan_products(product_jan)
            productImage = ProductImage.objects.filter(product_id=j_product.id, is_hidden=False)\
                .order_by('image_no').exclude(image_no__isnull=True).first()
            image_path = ''
            if productImage:
                image_path = productImage.image.image.url
            data = {
                "id": str(field.id),
                "date": field.order_product.order.order_date.strftime("%Y-%m-%d"),
                "image_path": image_path,
                "name": j_product.name,
                "amount": field.amount,
                "selling_price": field.order_product.total_price,
                "seller": field.order_product.order.seller.real_name if field.order_product.order.seller else ''
            }
            array.append(data)

    records_total = len(array)
    records_filtered = len(array)
    content = {"draw": draw, "data": array, "recordsTotal": records_total, "recordsFiltered": records_filtered}
    json_content = json.dumps(content, ensure_ascii=False)
    return HttpResponse(json_content, content_type='application/json')