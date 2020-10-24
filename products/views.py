from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Product, ProductImage, ProductCategory, ProductJancode, ProductVariety, ProductVarietySelection
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
        productImage = ProductImage.objects.filter(product_id=field.id, is_hidden=False).first()
        image_path = ''
        if productImage:
            image_path = productImage.image.image.url
        
        jancode_ids = get_products_jancodes(field.id, type='id')
        productJancodes = ProductJancode.objects.filter(id__in=jancode_ids)
        for p_jan in productJancodes:
            i = i + 1
            data = {
                "no": str(i),
                "jan_id": str(p_jan.id),
                "id": str(field.id),
                "name": str(field.name),
                "opened_date": field.opened_date.strftime("%Y-%m-%d"),
                "image_path": str(image_path),
                "jan_code": str(p_jan.jan_code),
                "stock": str(p_jan.stock)
            }
            
            array.append(data)

    content = {"draw": draw, "data": array, "recordsTotal": records_total, "recordsFiltered": records_filtered}
    json_content = json.dumps(content, ensure_ascii=False)
    return HttpResponse(json_content, content_type='application/json')


def get_products_jancodes(product_id, type='id'):
    product = Product.objects.get(pk=product_id)
    jancodes = []
    productVarieties = ProductVariety.objects.filter(product_id=product.id, is_hidden=False)
    for productVariety in productVarieties:
        productVarietySelections = ProductVarietySelection.objects.filter(product_variety_id=productVariety.id, is_hidden=False)
        for productVarietySelection in productVarietySelections:
            if productVariety.vertical_and_horizontal == 0:
                productJancodes = ProductJancode.objects.filter(horizontal_id=productVarietySelection.id, is_hidden=False)
                for productJancode in productJancodes:
                    if type == 'id':
                        if productJancode.id not in jancodes:
                            jancodes.append(productJancode.id)
                    elif type == 'code':
                        if productJancode.jan_code not in jancodes:
                            jancodes.append(productJancode.jan_code)
            else:
                productJancodes = ProductJancode.objects.filter(vertical_id=productVarietySelection.id, is_hidden=False)
                for productJancode in productJancodes:
                    if type == 'id':
                        if productJancode.id not in jancodes:
                            jancodes.append(productJancode.id)
                    elif type == 'code':
                        if productJancode.jan_code not in jancodes:
                            jancodes.append(productJancode.jan_code)

    return jancodes


# @login_required
def product_add(request):
    """
    Method to add new product.
    """

    if request.method == 'POST':
        try:
            product = Product()
            product.user_id = request.POST.get('profile_id')
            product.name = request.POST.get('name')
            product.brand_name = request.POST.get('brand_name')
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
            if product.variety == 0: # None
                obj = varities[0]
                productVariety = ProductVariety()
                productVariety.name = ''
                productVariety.vertical_and_horizontal = 0
                productVariety.product_id = product.id
                productVariety.save()

                productVarietySelection = ProductVarietySelection()
                productVarietySelection.selection = ''
                productVarietySelection.product_variety_id = productVariety.id
                productVarietySelection.save()

                productJancode = ProductJancode()
                productJancode.jan_code = obj['jan_code']
                productJancode.stock = obj['stock']
                productJancode.horizontal_id = productVarietySelection.id
                productJancode.save()
            else:
                if product.variety == 1: # Horizontal or vertical
                    for obj in varities:
                        obj_varities = obj['varities']
                        productVariety = ProductVariety()
                        productVariety.name = obj_varities[0]['name']
                        productVariety.vertical_and_horizontal = int(obj_varities[0]['vertical_and_horizontal'])
                        productVariety.product_id = product.id
                        productVariety.save()

                        productVarietySelection = ProductVarietySelection()
                        productVarietySelection.selection = obj_varities[0]['selection']
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
                elif product.variety == 2:  # Horizontal and vertical
                    for obj in varities:
                        obj_varities = obj['varities']
                        productVariety1 = ProductVariety()
                        productVariety1.name = obj_varities[0]['name']
                        productVariety1.vertical_and_horizontal = int(obj_varities[0]['vertical_and_horizontal'])
                        productVariety1.product_id = product.id
                        productVariety1.save()

                        productVariety2 = ProductVariety()
                        productVariety2.name = obj_varities[1]['name']
                        productVariety2.vertical_and_horizontal = int(obj_varities[1]['vertical_and_horizontal'])
                        productVariety2.product_id = product.id
                        productVariety2.save()

                        productVarietySelection1 = ProductVarietySelection()
                        productVarietySelection1.selection = obj_varities[0]['selection']
                        productVarietySelection1.product_variety_id = productVariety1.id
                        productVarietySelection1.save()
                        productVarietySelection2 = ProductVarietySelection()
                        productVarietySelection2.selection = obj_varities[1]['selection']
                        productVarietySelection2.product_variety_id = productVariety2.id
                        productVarietySelection2.save()

                        productJancode = ProductJancode()
                        productJancode.jan_code = obj['jan_code']
                        productJancode.stock = obj['stock']
                        productJancode.horizontal_id = productVarietySelection1.id
                        productJancode.vertical_id = productVarietySelection2.id
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
            product.brand_name = request.POST.get('brand_name')
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
            if product.variety == 0: # None
                obj = varities[0]
                productVariety = ProductVariety()
                productVariety.name = ''
                productVariety.vertical_and_horizontal = 0
                productVariety.product_id = product.id
                productVariety.save()

                productVarietySelection = ProductVarietySelection()
                productVarietySelection.selection = ''
                productVarietySelection.product_variety_id = productVariety.id
                productVarietySelection.save()

                productJancode = ProductJancode()
                productJancode.jan_code = obj['jan_code']
                productJancode.stock = obj['stock']
                productJancode.horizontal_id = productVarietySelection.id
                productJancode.save()
            else:
                if product.variety == 1: # Horizontal or vertical
                    for obj in varities:
                        obj_varities = obj['varities']
                        productVariety = ProductVariety()
                        productVariety.name = obj_varities[0]['name']
                        productVariety.vertical_and_horizontal = int(obj_varities[0]['vertical_and_horizontal'])
                        productVariety.product_id = product.id
                        productVariety.save()

                        productVarietySelection = ProductVarietySelection()
                        productVarietySelection.selection = obj_varities[0]['selection']
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
                elif product.variety == 2:  # Horizontal and vertical
                    for obj in varities:
                        obj_varities = obj['varities']
                        productVariety1 = ProductVariety()
                        productVariety1.name = obj_varities[0]['name']
                        productVariety1.vertical_and_horizontal = int(obj_varities[0]['vertical_and_horizontal'])
                        productVariety1.product_id = product.id
                        productVariety1.save()

                        productVariety2 = ProductVariety()
                        productVariety2.name = obj_varities[1]['name']
                        productVariety2.vertical_and_horizontal = int(obj_varities[1]['vertical_and_horizontal'])
                        productVariety2.product_id = product.id
                        productVariety2.save()

                        productVarietySelection1 = ProductVarietySelection()
                        productVarietySelection1.selection = obj_varities[0]['selection']
                        productVarietySelection1.product_variety_id = productVariety1.id
                        productVarietySelection1.save()
                        productVarietySelection2 = ProductVarietySelection()
                        productVarietySelection2.selection = obj_varities[1]['selection']
                        productVarietySelection2.product_variety_id = productVariety2.id
                        productVarietySelection2.save()

                        productJancode = ProductJancode()
                        productJancode.jan_code = obj['jan_code']
                        productJancode.stock = obj['stock']
                        productJancode.horizontal_id = productVarietySelection1.id
                        productJancode.vertical_id = productVarietySelection2.id
                        productJancode.save()

            return render(request, 'product_list.html')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, e, extra_tags='product_edit')

    product = Product.objects.get(pk=product_id)

    image_array = []
    productImages = ProductImage.objects.filter(product_id=product.id, is_hidden=False)
    for productImage in productImages:
        image_array.append(productImage.image.image.url)


    p_varities = []
    jancode_ids = get_products_jancodes(product.id, type='id')
    for jan_id in jancode_ids:
        varities = []
        productJancode = ProductJancode.objects.get(pk=jan_id)
        if productJancode.horizontal_id:
            productVarietySelection = ProductVarietySelection.objects.get(pk=productJancode.horizontal_id)
            productVariety = ProductVariety.objects.get(pk=productVarietySelection.product_variety_id)
            varities.append({
                "name": str(productVariety.name),
                "selection": str(productVarietySelection.selection),
                "vertical_and_horizontal": str(productVariety.vertical_and_horizontal),
            })
        if productJancode.vertical_id:
            productVarietySelection = ProductVarietySelection.objects.get(pk=productJancode.vertical_id)
            productVariety = ProductVariety.objects.get(pk=productVarietySelection.product_variety_id)
            varities.append({
                "name": str(productVariety.name),
                "selection": str(productVarietySelection.selection),
                "vertical_and_horizontal": str(productVariety.vertical_and_horizontal),
            })
        p_varities.append({
            "jan_code": str(productJancode.jan_code),
            "stock": str(productJancode.stock),
            "varities": varities
        })

    category_list = list(ProductCategory.objects.filter(is_hidden=False).values_list('id', 'name'))

    return render(request, 'product_form.html', {'product': product,
                                                'images': image_array,
                                                'varities': p_varities,
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

        jancode_ids = get_products_jancodes(product.id, type='id')
        productJancodes = ProductJancode.objects.filter(id__in=jancode_ids).update(is_hidden=True, modified=datetime.datetime.now())
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
                product.brand_name = request.POST.get('brand_name')
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
                if product.variety == 0: # None
                    obj = varities[0]
                    productVariety = ProductVariety()
                    productVariety.name = ''
                    productVariety.vertical_and_horizontal = 0
                    productVariety.product_id = product.id
                    productVariety.save()

                    productVarietySelection = ProductVarietySelection()
                    productVarietySelection.selection = ''
                    productVarietySelection.product_variety_id = productVariety.id
                    productVarietySelection.save()

                    productJancode = ProductJancode()
                    productJancode.jan_code = obj['jan_code']
                    productJancode.stock = obj['stock']
                    productJancode.horizontal_id = productVarietySelection.id
                    productJancode.save()
                else:
                    if product.variety == 1: # Horizontal or vertical
                        for obj in varities:
                            obj_varities = obj['varities']
                            productVariety = ProductVariety()
                            productVariety.name = obj_varities[0]['name']
                            productVariety.vertical_and_horizontal = int(obj_varities[0]['vertical_and_horizontal'])
                            productVariety.product_id = product.id
                            productVariety.save()

                            productVarietySelection = ProductVarietySelection()
                            productVarietySelection.selection = obj_varities[0]['selection']
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
                    elif product.variety == 2:  # Horizontal and vertical
                        for obj in varities:
                            obj_varities = obj['varities']
                            productVariety1 = ProductVariety()
                            productVariety1.name = obj_varities[0]['name']
                            productVariety1.vertical_and_horizontal = int(obj_varities[0]['vertical_and_horizontal'])
                            productVariety1.product_id = product.id
                            productVariety1.save()

                            productVariety2 = ProductVariety()
                            productVariety2.name = obj_varities[1]['name']
                            productVariety2.vertical_and_horizontal = int(obj_varities[1]['vertical_and_horizontal'])
                            productVariety2.product_id = product.id
                            productVariety2.save()

                            productVarietySelection1 = ProductVarietySelection()
                            productVarietySelection1.selection = obj_varities[0]['selection']
                            productVarietySelection1.product_variety_id = productVariety1.id
                            productVarietySelection1.save()
                            productVarietySelection2 = ProductVarietySelection()
                            productVarietySelection2.selection = obj_varities[1]['selection']
                            productVarietySelection2.product_variety_id = productVariety2.id
                            productVarietySelection2.save()

                            productJancode = ProductJancode()
                            productJancode.jan_code = obj['jan_code']
                            productJancode.stock = obj['stock']
                            productJancode.horizontal_id = productVarietySelection1.id
                            productJancode.vertical_id = productVarietySelection2.id
                            productJancode.save()
            else:
                product = Product()
                product.user_id = request.POST.get('profile_id')
                product.name = request.POST.get('name')
                product.brand_name = request.POST.get('brand_name')
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
                if product.variety == 0: # None
                    obj = varities[0]
                    productVariety = ProductVariety()
                    productVariety.name = ''
                    productVariety.vertical_and_horizontal = 0
                    productVariety.product_id = product.id
                    productVariety.save()

                    productVarietySelection = ProductVarietySelection()
                    productVarietySelection.selection = ''
                    productVarietySelection.product_variety_id = productVariety.id
                    productVarietySelection.save()

                    productJancode = ProductJancode()
                    productJancode.jan_code = obj['jan_code']
                    productJancode.stock = obj['stock']
                    productJancode.horizontal_id = productVarietySelection.id
                    productJancode.save()
                else:
                    if product.variety == 1: # Horizontal or vertical
                        for obj in varities:
                            obj_varities = obj['varities']
                            productVariety = ProductVariety()
                            productVariety.name = obj_varities[0]['name']
                            productVariety.vertical_and_horizontal = int(obj_varities[0]['vertical_and_horizontal'])
                            productVariety.product_id = product.id
                            productVariety.save()

                            productVarietySelection = ProductVarietySelection()
                            productVarietySelection.selection = obj_varities[0]['selection']
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
                    elif product.variety == 2:  # Horizontal and vertical
                        for obj in varities:
                            obj_varities = obj['varities']
                            productVariety1 = ProductVariety()
                            productVariety1.name = obj_varities[0]['name']
                            productVariety1.vertical_and_horizontal = int(obj_varities[0]['vertical_and_horizontal'])
                            productVariety1.product_id = product.id
                            productVariety1.save()

                            productVariety2 = ProductVariety()
                            productVariety2.name = obj_varities[1]['name']
                            productVariety2.vertical_and_horizontal = int(obj_varities[1]['vertical_and_horizontal'])
                            productVariety2.product_id = product.id
                            productVariety2.save()

                            productVarietySelection1 = ProductVarietySelection()
                            productVarietySelection1.selection = obj_varities[0]['selection']
                            productVarietySelection1.product_variety_id = productVariety1.id
                            productVarietySelection1.save()
                            productVarietySelection2 = ProductVarietySelection()
                            productVarietySelection2.selection = obj_varities[1]['selection']
                            productVarietySelection2.product_variety_id = productVariety2.id
                            productVarietySelection2.save()

                            productJancode = ProductJancode()
                            productJancode.jan_code = obj['jan_code']
                            productJancode.stock = obj['stock']
                            productJancode.horizontal_id = productVarietySelection1.id
                            productJancode.vertical_id = productVarietySelection2.id
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
        'brand_name': '',
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
                    'brand_name': product.brand_name,
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

                p_varities = []
                jancode_ids = get_products_jancodes(product.id, type='id')
                for jan_id in jancode_ids:
                    varities = []
                    productJancode = ProductJancode.objects.get(pk=jan_id)
                    if productJancode.horizontal_id:
                        productVarietySelection = ProductVarietySelection.objects.get(pk=productJancode.horizontal_id)
                        productVariety = ProductVariety.objects.get(pk=productVarietySelection.product_variety_id)
                        varities.append({
                            "name": str(productVariety.name),
                            "selection": str(productVarietySelection.selection),
                            "vertical_and_horizontal": str(productVariety.vertical_and_horizontal),
                        })
                    if productJancode.vertical_id:
                        productVarietySelection = ProductVarietySelection.objects.get(pk=productJancode.vertical_id)
                        productVariety = ProductVariety.objects.get(pk=productVarietySelection.product_variety_id)
                        varities.append({
                            "name": str(productVariety.name),
                            "selection": str(productVarietySelection.selection),
                            "vertical_and_horizontal": str(productVariety.vertical_and_horizontal),
                        })
                    p_varities.append({
                        "jan_code": str(productJancode.jan_code),
                        "stock": str(productJancode.stock),
                        "varities": varities
                    })
                context['varities'] = p_varities

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

            jancode_ids = get_products_jancodes(product.id, type='id')
            productJancodes = ProductJancode.objects.filter(id__in=jancode_ids).update(is_hidden=True, modified=datetime.datetime.now())

            message = 'Success'
        except Exception as e:
            print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")