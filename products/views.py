from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.urls import reverse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import Product, ProductImage, ProductCategory, ProductJancode, ProductVariety, ProductVarietySelection
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

    product_list = Product.objects.filter(is_hidden=False).order_by('name')
    filter_array = eval(request.GET.get('filter_str'))
    if len(filter_array):
        if 1 not in filter_array:
            product_list = product_list.exclude(is_opened=True)
        if 2 not in filter_array:
            product_list = product_list.exclude(is_opened=False)
        if 3 not in filter_array:
            product_list = product_list.exclude(is_draft=True)
        
    records_total = product_list.count()

    if search:  # Filter data base on search
        product_list = product_list.filter(Q(name__icontains=search)).order_by('name')

    # All data
    records_filtered = product_list.count()
    # Order by list_limit base on order_dir and order_column
    order_column = request.GET['order[0][column]']
    column_name = ""
    if order_column == "2":
        column_name = "name"
    
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

        productImage = ProductImage.objects.filter(product_id=field.id, is_hidden=False).first()
        image_path = ''
        if productImage:
            image_path = productImage.image.image.url
        data = {
            "no": str(i),
            "id": str(field.id),
            "name": str(field.name),
            "opened_date": str(field.opened_date),
            "image_path": str(image_path),
            "jan_code": '',
            "stock": ''
        }
        productVarieties = ProductVariety.objects.filter(product_id=field.id)
        for productVariety in productVarieties:
            productVarietySelections = ProductVarietySelection.objects.filter(product_variety_id=productVariety.id)
            for productVarietySelection in productVarietySelections:
                productJancodes = ProductJancode.objects.filter(horizontal_id=productVarietySelection.id)
                for productJancode in productJancodes:
                    data["jan_code"] = str(productJancode.jan_code)
                    data["stock"] = str(productJancode.stock)
        
        array.append(data)

    content = {"draw": draw, "data": array, "recordsTotal": records_total, "recordsFiltered": records_filtered}
    json_content = json.dumps(content, ensure_ascii=False)
    return HttpResponse(json_content, content_type='application/json')


# @login_required
def product_add(request):
    """
    Method to add new product.
    """
    varities = [
            {
                "name": "size",
                "selection": "small",
                "jan_code": "small",
                "stock": "5",
                "vertical_and_horizontal": "0" # 0=horizontal, 1=vertical
            },
            {
                "name": "color",
                "selection": "red",
                "jan_code": "red",
                "stock": "5",
                "vertical_and_horizontal": "1" # 0=horizontal, 1=vertical
            }
        ]

    if request.method == 'POST':
        try:
            product = Product()
            product.name = request.POST.get('name')
            product.barnd_name = request.POST.get('barnd_name')
            product.description = request.POST.get('description')
            product.pr = request.POST.get('pr')
            product.url_str = request.POST.get('url_str')
            product.category_id = request.POST.get('category')
            product.target = request.POST.get('target')
            product.price = request.POST.get('price')
            product.store_price = request.POST.get('store_price')
            product.shipping_fee = request.POST.get('shipping_fee')
            product.opened_date = request.POST.get('opened_date')
            product.is_opened = int(request.POST.get('is_opened'))
            product.is_used = int(request.POST.get('is_used'))
            product.is_draft = int(request.POST.get('is_draft'))
            product.variety = int(request.POST.get('variety'))
            product.save()

            # product image save 
            image_ids = []
            product_images = request.FILES.getlist('product_image')
            for image in product_images:
                new_image = Image()
                new_image.image.save(image.name, image)
                new_image.save()
                image_ids.append(new_image.id)
            
            for image_id in image_ids:
                productImage = ProductImage()
                productImage.image_id = image_id
                productImage.product_id = product.id
                productImage.save()

            # save product varieties
            varities = json.loads(request.POST.get('varities'))
            for obj in varities:
                productVariety = ProductVariety()
                productVariety.name = obj['name']
                productVariety.vertical_and_horizontal = int(obj['vertical_and_horizontal'])
                productVariety.product_id = product.id
                productVariety.save()

                productVarietySelection = ProductVarietySelection()
                productVarietySelection.selection = obj['selection']
                productVarietySelection.product_variety_id = productVariety.id
                productVarietySelection.save()

                productJancode = ProductJancode()
                productJancode.jan_code = obj['jan_code']
                productJancode.stock = obj['stock']
                if productVariety.vertical_and_horizontal == 0:
                    productJancode.horizontal_id = productVarietySelection.id
                else:
                    productJancode.vertical_id = productVarietySelection.id
                productJancode.save()

            return render(request, 'product_list.html')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, e, extra_tags='product_add')

    category_list = list(ProductCategory.objects.filter(is_hidden=False).values_list('id', 'name'))
    return render(request, 'product_form.html', {'category_list': category_list, 'media_url': s.MEDIA_URL})


# @login_required
def product_edit(request, product_id):
    """
    Method to edit a product.
    """

    if request.method == 'POST':
        try:
            product = Product.objects.get(pk=product_id)
            product.name = request.POST.get('name')
            product.barnd_name = request.POST.get('barnd_name')
            product.description = request.POST.get('description')
            product.pr = request.POST.get('pr')
            product.url_str = request.POST.get('url_str')
            product.category_id = request.POST.get('category')
            product.target = request.POST.get('target')
            product.price = request.POST.get('price')
            product.store_price = request.POST.get('store_price')
            product.shipping_fee = request.POST.get('shipping_fee')
            product.opened_date = request.POST.get('opened_date')
            product.is_opened = int(request.POST.get('is_opened'))
            product.is_used = int(request.POST.get('is_used'))
            product.is_draft = int(request.POST.get('is_draft'))
            product.variety = int(request.POST.get('variety'))
            product.modified = datetime.datetime.now()
            product.save()

            # product old image delete 
            productImages = ProductImage.objects.filter(product_id=product.id, is_hidden=False)
            for productImage in productImages:
                # may be CASCADE will do it
                # image = Image.objects.get(pk=productImage.image_id)
                # image.delete()

                productImage.delete()
            
            # product new image save 
            image_ids = []
            product_images = request.FILES.getlist('product_image')
            for image in product_images:
                new_image = Image()
                new_image.image.save(image.name, image)
                new_image.save()
                image_ids.append(new_image.id)
            
            for image_id in image_ids:
                productImage = ProductImage()
                productImage.image_id = image_id
                productImage.product_id = product.id
                productImage.save()

            # delete product old varieties
            productVarieties = ProductVariety.objects.filter(product_id=product.id)
            for productVariety in productVarieties:
                # may be CASCADE will do it
                # productVarietySelections = ProductVarietySelection.objects.filter(product_variety_id=productVariety.id)
                # for productVarietySelection in productVarietySelections:
                #     productJancodes = ProductJancode.objects.filter(horizontal_id=productVarietySelection.id)
                #     for productJancode in productJancodes:
                #         productJancode.delete()
                #     productJancodes = ProductJancode.objects.filter(vertical_id=productVarietySelection.id)
                #     for productJancode in productJancodes:
                #         productJancode.delete()

                #     productVarietySelection.delete()
                    
                productVariety.delete()

            # save product new varieties
            varities = json.loads(request.POST.get('varities'))
            for obj in varities:
                productVariety = ProductVariety()
                productVariety.name = obj['name']
                productVariety.vertical_and_horizontal = int(obj['vertical_and_horizontal'])
                productVariety.product_id = product.id
                productVariety.save()

                productVarietySelection = ProductVarietySelection()
                productVarietySelection.selection = obj['selection']
                productVarietySelection.product_variety_id = productVariety.id
                productVarietySelection.save()

                productJancode = ProductJancode()
                productJancode.jan_code = obj['jan_code']
                productJancode.stock = obj['stock']
                if productVariety.vertical_and_horizontal == 0:
                    productJancode.horizontal_id = productVarietySelection.id
                else:
                    productJancode.vertical_id = productVarietySelection.id
                productJancode.save()

            return render(request, 'product_list.html')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, e, extra_tags='product_edit')

    product = Product.objects.get(pk=product_id)
    category_list = list(ProductCategory.objects.filter(is_hidden=False).values_list('id', 'name'))
    return render(request, 'product_form.html', {"product": product,
                                                'category_list': category_list,
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


@csrf_exempt
def add_update_product(request):
    """
    ajax Method to add or update a product.
    """

    message = 'Error'
    if request.method == 'POST':
        try:
            if request.POST.get('product_id') and request.POST.get('product_id') != '':
                product_id = request.POST.get('product_id')
                product = Product.objects.get(pk=product_id)
                product.name = request.POST.get('name')
                product.barnd_name = request.POST.get('barnd_name')
                product.description = request.POST.get('description')
                product.pr = request.POST.get('pr')
                product.url_str = request.POST.get('url_str')
                product.category_id = request.POST.get('category')
                product.target = request.POST.get('target')
                product.price = request.POST.get('price')
                product.store_price = request.POST.get('store_price')
                product.shipping_fee = request.POST.get('shipping_fee')
                product.opened_date = request.POST.get('opened_date')
                product.is_opened = int(request.POST.get('is_opened'))
                product.is_used = int(request.POST.get('is_used'))
                product.is_draft = int(request.POST.get('is_draft'))
                product.variety = int(request.POST.get('variety'))
                product.modified = datetime.datetime.now()
                product.save()

                # product old image delete 
                productImages = ProductImage.objects.filter(product_id=product.id, is_hidden=False)
                for productImage in productImages:
                    # may be CASCADE will do it
                    # image = Image.objects.get(pk=productImage.image_id)
                    # image.delete()

                    productImage.delete()
                
                # product new image save 
                image_ids = []
                product_images = request.FILES.getlist('product_image')
                for image in product_images:
                    new_image = Image()
                    new_image.image.save(image.name, image)
                    new_image.save()
                    image_ids.append(new_image.id)
                
                for image_id in image_ids:
                    productImage = ProductImage()
                    productImage.image_id = image_id
                    productImage.product_id = product.id
                    productImage.save()

                # delete product old varieties
                productVarieties = ProductVariety.objects.filter(product_id=product.id)
                for productVariety in productVarieties:
                    # may be CASCADE will do it
                    # productVarietySelections = ProductVarietySelection.objects.filter(product_variety_id=productVariety.id)
                    # for productVarietySelection in productVarietySelections:
                    #     productJancodes = ProductJancode.objects.filter(horizontal_id=productVarietySelection.id)
                    #     for productJancode in productJancodes:
                    #         productJancode.delete()
                    #     productJancodes = ProductJancode.objects.filter(vertical_id=productVarietySelection.id)
                    #     for productJancode in productJancodes:
                    #         productJancode.delete()

                    #     productVarietySelection.delete()
                        
                    productVariety.delete()

                # save product new varieties
                varities = json.loads(request.POST.get('varities'))
                for obj in varities:
                    productVariety = ProductVariety()
                    productVariety.name = obj['name']
                    productVariety.vertical_and_horizontal = int(obj['vertical_and_horizontal'])
                    productVariety.product_id = product.id
                    productVariety.save()

                    productVarietySelection = ProductVarietySelection()
                    productVarietySelection.selection = obj['selection']
                    productVarietySelection.product_variety_id = productVariety.id
                    productVarietySelection.save()

                    productJancode = ProductJancode()
                    productJancode.jan_code = obj['jan_code']
                    productJancode.stock = obj['stock']
                    if productVariety.vertical_and_horizontal == 0:
                        productJancode.horizontal_id = productVarietySelection.id
                    else:
                        productJancode.vertical_id = productVarietySelection.id
                    productJancode.save()
            else:
                product = Product()
                product.name = request.POST.get('name')
                product.barnd_name = request.POST.get('barnd_name')
                product.description = request.POST.get('description')
                product.pr = request.POST.get('pr')
                product.url_str = request.POST.get('url_str')
                product.category_id = request.POST.get('category')
                product.target = request.POST.get('target')
                product.price = request.POST.get('price')
                product.store_price = request.POST.get('store_price')
                product.shipping_fee = request.POST.get('shipping_fee')
                product.opened_date = request.POST.get('opened_date')
                product.is_opened = int(request.POST.get('is_opened'))
                product.is_used = int(request.POST.get('is_used'))
                product.is_draft = int(request.POST.get('is_draft'))
                product.variety = int(request.POST.get('variety'))
                product.save()

                # product image save 
                image_ids = []
                product_images = request.FILES.getlist('product_image')
                for image in product_images:
                    new_image = Image()
                    new_image.image.save(image.name, image)
                    new_image.save()
                    image_ids.append(new_image.id)
                
                for image_id in image_ids:
                    productImage = ProductImage()
                    productImage.image_id = image_id
                    productImage.product_id = product.id
                    productImage.save()

                # save product varieties
                varities = json.loads(request.POST.get('varities'))
                for obj in varities:
                    productVariety = ProductVariety()
                    productVariety.name = obj['name']
                    productVariety.vertical_and_horizontal = int(obj['vertical_and_horizontal'])
                    productVariety.product_id = product.id
                    productVariety.save()

                    productVarietySelection = ProductVarietySelection()
                    productVarietySelection.selection = obj['selection']
                    productVarietySelection.product_variety_id = productVariety.id
                    productVarietySelection.save()

                    productJancode = ProductJancode()
                    productJancode.jan_code = obj['jan_code']
                    productJancode.stock = obj['stock']
                    if productVariety.vertical_and_horizontal == 0:
                        productJancode.horizontal_id = productVarietySelection.id
                    else:
                        productJancode.vertical_id = productVarietySelection.id
                    productJancode.save()

            message = 'Success'
        except Exception as e:
            print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")


@csrf_exempt
def get_product_info(request):
    """
    ajax Method to get a product info
    """

    context = {
        'name': '',
        'barnd_name': '',
        'description': '',
        'pr': '',
        'url_str': '',
        'category': '',
        'target': '',
        'price': '',
        'store_price': '',
        'shipping_fee': '',
        'opened_date': '',
        'is_opened': '',
        'is_used': '',
        'is_draft': '',
        'images': '',
        'variety': '',
        'varieties': '[]',
    }
    message = 'Error'
    if request.method == 'POST':
        try:
            if request.POST.get('product_id') and request.POST.get('product_id') != '':
                product_id = request.POST.get('product_id')
                product = Product.objects.get(pk=product_id)
                context = {
                    'name': product.name,
                    'barnd_name': product.barnd_name,
                    'description': product.description,
                    'pr': product.pr,
                    'url_str': product.url_str,
                    'category': product.category_id,
                    'target': product.target,
                    'price': product.price,
                    'store_price': product.store_price,
                    'shipping_fee': product.shipping_fee,
                    'opened_date': product.opened_date,
                    'is_opened': '1' if product.is_opened else '0',
                    'is_used': '1' if product.is_used else '0',
                    'is_draft': '1' if product.is_draft else '0',
                    'variety': product.variety,
                }
                image_array = []
                productImages = ProductImage.objects.filter(product_id=product.id, is_hidden=False)
                for productImage in productImages:
                    image_array.append(productImage.image.image.url)

                context['images'] = image_array

                varities = []
                productVarieties = ProductVariety.objects.filter(product_id=product.id)
                for productVariety in productVarieties:
                    productVarietySelections = ProductVarietySelection.objects.filter(product_variety_id=productVariety.id)
                    for productVarietySelection in productVarietySelections:
                        productJancodes = ProductJancode.objects.filter(horizontal_id=productVarietySelection.id)
                        for productJancode in productJancodes:
                            varities.append({
                                "name": productVariety.name,
                                "vertical_and_horizontal": productVariety.vertical_and_horizontal,
                                "selection": productVarietySelection.selection,
                                "jan_code": productJancode.jan_code,
                                "stock": productJancode.stock,
                            })
                context['varities'] = varities

            message = 'Success'
        except Exception as e:
            print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")


@csrf_exempt
def delete_product(request):
    """
    ajax Method to delete a product.
    """

    message = 'Error'
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
            product.is_hidden = 1
            product.modified = datetime.datetime.now()
            product.save()

            message = 'Success'
        except Exception as e:
            print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")