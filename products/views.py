import datetime
import json
import csv
from django.conf import settings as s
from django.contrib import messages
from django.db.models import Q
from django.contrib.humanize.templatetags.humanize import intcomma
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.utils import translation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Product, ProductImage, ProductCategory, ProductJancode, ProductVariety, ProductVarietySelection
from images.models import Image
from profiles.models import Profile
from utilities.constants import AUTHORITY_TYPE


@login_required
def product_list(request):
    """
    Method to redirect to product list page.
    """

    if request.session['login_type'] == 'SELLER':
        try:
            profile_id = request.session['login_profile_id']
        except Exception as e:
            print(e)
            profile_id = ''

        return render(request, 'product_list.html', {'profile_id': profile_id})
    else:
        return render(request, '404.html')


# @login_required
@csrf_exempt
def ProductList__asJson(request):
    """
    Method to get product list as JSON.
    """

    draw = request.GET['draw']
    start = request.GET['start']
    length = request.GET['length']
    search = request.GET['search[value]']

    profile_id = request.GET.get('profile_id')
    if not profile_id:
        profile_id = request.session['login_profile_id']
    product_list = Product.objects.filter(is_hidden=False, user_id=profile_id).order_by('name')
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
        product_list = product_list.filter(
            Q(name__icontains=search)).order_by('name')

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
        productImage = ProductImage.objects.filter(
            product_id=field.id, is_hidden=False).order_by('image_no').exclude(image_no__isnull=True).first()
        image_path = ''
        if productImage:
            image_path = productImage.image.image.url
            image_path = image_path.split('?')[0]

        jancode_ids = get_products_jancodes(field.id, type='id')
        productJancodes = ProductJancode.objects.filter(id__in=jancode_ids)
        for p_jan in productJancodes:
            veries = get_jan_varieties(p_jan)
            very_str = ''
            for item in veries:
                if item['name']:
                    very_str += item['name'] + ' : ' + item['selection'] + ','
            if len(very_str):
                very_str = very_str[:-1]
            else:
                language = translation.get_language()
                if language == 'ja':
                    very_str = '無し'
                else:
                    very_str = 'None'
            i = i + 1
            # print(vars(field))
            data = {
                "no": str(i),
                "jan_id": str(p_jan.id),
                "id": str(field.id),
                "name": str(field.name),
                "price": field.price,
                "opened_date": field.opened_date.strftime("%Y-%m-%d") if field.opened_date else '',
                "image_path": str(image_path),
                "jan_code": str(p_jan.jan_code),
                "stock": str(p_jan.stock),
                "varieties": very_str
            }

            array.append(data)
    records_total = len(array)
    records_filtered = len(array)
    content = {"draw": draw, "data": array,
               "recordsTotal": records_total, "recordsFiltered": records_filtered}
    json_content = json.dumps(content, ensure_ascii=False)
    return HttpResponse(json_content, content_type='application/json')


def SellerProductList__asJson(request):
    """
    Method to get seller product list as JSON.
    """

    profile_id = request.GET.get('seller_id')
    if not profile_id:
        profile_id = request.session['login_profile_id']
    product_list = Product.objects.filter(is_hidden=False, user_id=profile_id, is_opened=True).order_by('name')

    array = []
    i = 0
    for field in product_list:
        productImage = ProductImage.objects.filter(
            product_id=field.id, is_hidden=False).order_by('image_no').exclude(image_no__isnull=True).first()
        image_path = ''
        if productImage:
            image_path = productImage.image.image.url

        jancode_ids = get_products_jancodes(field.id, type='id')
        productJancodes = ProductJancode.objects.filter(id__in=jancode_ids).exclude(stock__isnull=True).exclude(stock__lte=0)
        for p_jan in productJancodes:
            veries = get_jan_varieties(p_jan)
            very_str = ''
            for item in veries:
                if item['name']:
                    very_str += item['selection'] + ','
            if len(very_str):
                very_str = very_str[:-1]
            i = i + 1
            data = {
                "no": str(i),
                "jan_id": str(p_jan.id),
                "id": str(field.id),
                "name": str(field.name),
                "opened_date": field.opened_date.strftime("%Y-%m-%d") if field.opened_date else '',
                "image_path": str(image_path),
                "jan_code": str(p_jan.jan_code),
                "stock": str(p_jan.stock),
                "price": str(field.price),
                "store_price": str(field.store_price),
                "varieties": very_str
            }

            array.append(data)
    content = {"data": array,}
    json_content = json.dumps(content, ensure_ascii=False)
    return HttpResponse(json_content, content_type='application/json')


def check_for_duplicate(request, type, value):
    """
    Method to verify duplcate info.
    """

    message = 'Error'
    try:
        product = None
        if type == 'url_str':
            product = Product.objects.filter(url_str=value).first()
        # elif type == '':
        #     product = Product.objects.filter(user_code=value).first()

        if product:
            message = 'Success'
    except Exception as e:
        print(e)

    context = { 'message': message }
    return HttpResponse(json.dumps(context), content_type="application/json")


def get_jan_products(productJancode):
    """
    Method to get the Product by Jancode Object.
    """

    product = None
    try:
        if productJancode.horizontal_id:
            productVarietySelection = ProductVarietySelection.objects.get(
                pk=productJancode.horizontal_id)
            productVariety = ProductVariety.objects.get(
                pk=productVarietySelection.product_variety_id)
            product = Product.objects.get(pk=productVariety.product_id)

        if productJancode.vertical_id:
            productVarietySelection = ProductVarietySelection.objects.get(
                pk=productJancode.vertical_id)
            productVariety = ProductVariety.objects.get(
                pk=productVarietySelection.product_variety_id)
            product = Product.objects.get(pk=productVariety.product_id)

    except Exception as e:
        print('get_jan_products', e)

    return product


def get_jan_varieties(productJancode):
    """
    Method to get the varieties of a product by Jancode Object.
    """

    varieties = []
    try:
        if productJancode.horizontal_id:
            productVarietySelection = ProductVarietySelection.objects.get(
                pk=productJancode.horizontal_id)
            productVariety = ProductVariety.objects.get(
                pk=productVarietySelection.product_variety_id)
            varieties.append({
                "name": str(productVariety.name),
                "selection": str(productVarietySelection.selection),
                "vertical_and_horizontal": str(productVariety.vertical_and_horizontal),
            })
        if productJancode.vertical_id:
            productVarietySelection = ProductVarietySelection.objects.get(
                pk=productJancode.vertical_id)
            productVariety = ProductVariety.objects.get(
                pk=productVarietySelection.product_variety_id)
            varieties.append({
                "name": str(productVariety.name),
                "selection": str(productVarietySelection.selection),
                "vertical_and_horizontal": str(productVariety.vertical_and_horizontal),
            })
    except Exception as e:
        print('get_jan_varieties', e)

    return varieties


def get_products_jancodes(product_id, type='id'):
    """
    Method to get the Jancodes list of a product.
    """

    jancodes = []
    try:
        product = Product.objects.get(pk=product_id)
        productVarieties = ProductVariety.objects.filter(
            product_id=product.id, is_hidden=False)
        for productVariety in productVarieties:
            productVarietySelections = ProductVarietySelection.objects.filter(
                product_variety_id=productVariety.id, is_hidden=False)
            for productVarietySelection in productVarietySelections:
                if productVariety.vertical_and_horizontal == 0:
                    productJancodes = ProductJancode.objects.filter(
                        horizontal_id=productVarietySelection.id, is_hidden=False)
                    for productJancode in productJancodes:
                        if type == 'id':
                            if productJancode.id not in jancodes:
                                jancodes.append(productJancode.id)
                        elif type == 'code':
                            if productJancode.jan_code not in jancodes:
                                jancodes.append(productJancode.jan_code)
                else:
                    productJancodes = ProductJancode.objects.filter(
                        vertical_id=productVarietySelection.id, is_hidden=False)
                    for productJancode in productJancodes:
                        if type == 'id':
                            if productJancode.id not in jancodes:
                                jancodes.append(productJancode.id)
                        elif type == 'code':
                            if productJancode.jan_code not in jancodes:
                                jancodes.append(productJancode.jan_code)

    except Exception as e:
        print('get_products_jancodes', e)

    return jancodes


@login_required
def product_add(request):
    """
    Method to add new product.
    """

    if request.session['login_type'] == 'SELLER':
        seller_id = request.session['login_profile_id']
        if request.method == 'POST':
            try:
                product = Product()
                product.user_id = seller_id
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
                product.is_used = int(request.POST.get('used'))
                product.is_draft = int(request.POST.get('draft'))
                product.variety = int(request.POST.get('sel_variety'))
                product.save()

                # product image save
                if request.FILES.get('product_image0', False):
                    save_product_image(request.FILES.get('product_image0'), 1, product.id)
                if request.FILES.get('product_image1', False):
                    save_product_image(request.FILES.get('product_image1'), 2, product.id)
                if request.FILES.get('product_image2', False):
                    save_product_image(request.FILES.get('product_image2'), 3, product.id)
                if request.FILES.get('product_image3', False):
                    save_product_image(request.FILES.get('product_image3'), 4, product.id)
                if request.FILES.get('product_image4', False):
                    save_product_image(request.FILES.get('product_image4'), 5, product.id)

                # save product varieties
                varieties = json.loads(request.POST.get('varieties'))
                saveNewVareities(product, varieties)

                return redirect('/products/product_list/')
            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR,
                                    e, extra_tags='product_add')

        seller_auth_id = Profile.objects.get(pk=seller_id).authority_id
        category_list = list(ProductCategory.objects.filter(
            is_hidden=False).values_list('id', 'name'))
        return render(request, 'product_form.html', {'category_list': category_list,
                                                    'media_url': s.MEDIA_URL,
                                                    'seller_auth_id': seller_auth_id})
    else:
        return render(request, '404.html')


@login_required
def product_edit(request, product_id):
    """
    Method to edit a product.
    """

    if request.session['login_type'] == 'SELLER':
        seller_id = request.session['login_profile_id']
        if request.method == 'POST':
            try:
                product = Product.objects.filter(pk=product_id, user_id=seller_id)
                if product.exists():
                    product = product.first()
                    last_variety_type = product.variety
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
                    product.is_used = int(request.POST.get('used'))
                    product.is_draft = int(request.POST.get('draft'))
                    product.variety = int(request.POST.get('sel_variety'))
                    product.modified = datetime.datetime.now()
                    product.save()

                    # product image update
                    if request.FILES.get('product_image0', False):
                        update_product_image(request.FILES.get('product_image0'), 1, product.id)
                    if request.FILES.get('product_image1', False):
                        update_product_image(request.FILES.get('product_image1'), 2, product.id)
                    if request.FILES.get('product_image2', False):
                        update_product_image(request.FILES.get('product_image2'), 3, product.id)
                    if request.FILES.get('product_image3', False):
                        update_product_image(request.FILES.get('product_image3'), 4, product.id)
                    if request.FILES.get('product_image4', False):
                        update_product_image(request.FILES.get('product_image4'), 5, product.id)

                    # remove selected image
                    deleted_images_list = json.loads(request.POST.get('image_delete'))
                    if len(deleted_images_list):
                        delete_product_images(product.id, deleted_images_list)

                    # check if variety type changes
                    # if so then delete 0ld data
                    if last_variety_type != product.variety:
                        deleteOldVarieties(product)

                    # save product new varieties
                    varieties = json.loads(request.POST.get('varieties'))
                    old_varieties = json.loads(request.POST.get('old_varieties'))
                    if last_variety_type != product.variety:
                        old_varieties = []
                    updateProductVarieties(product, product.variety, varieties, old_varieties)

                    return redirect('/products/product_list/')
            except Exception as e:
                print(e)
                messages.add_message(request, messages.ERROR,
                                    e, extra_tags='product_edit')

        image_array = []
        product = Product.objects.filter(pk=product_id, user_id=seller_id)
        if product.exists():
            product = product.first()

            productImages = ProductImage.objects.filter(
                product_id=product.id, is_hidden=False).order_by('image_no').exclude(image_no__isnull=True)
            for productImage in productImages:
                image_array.append(productImage.image.image.url)

            # p_varieties = []
            # jancode_ids = get_products_jancodes(product.id, type='id')
            # for jan_id in jancode_ids:
            #     varieties = []
            #     productJancode = ProductJancode.objects.get(pk=jan_id)
            #     if productJancode.horizontal_id:
            #         productVarietySelection = ProductVarietySelection.objects.get(
            #             pk=productJancode.horizontal_id)
            #         productVariety = ProductVariety.objects.get(
            #             pk=productVarietySelection.product_variety_id)
            #         varieties.append({
            #             "name": str(productVariety.name),
            #             "selection": str(productVarietySelection.selection),
            #             "vertical_and_horizontal": str(productVariety.vertical_and_horizontal),
            #         })
            #     if productJancode.vertical_id:
            #         productVarietySelection = ProductVarietySelection.objects.get(
            #             pk=productJancode.vertical_id)
            #         productVariety = ProductVariety.objects.get(
            #             pk=productVarietySelection.product_variety_id)
            #         varieties.append({
            #             "name": str(productVariety.name),
            #             "selection": str(productVarietySelection.selection),
            #             "vertical_and_horizontal": str(productVariety.vertical_and_horizontal),
            #         })
            #     p_varieties.append({
            #         "jan_code": str(productJancode.jan_code),
            #         "stock": str(productJancode.stock),
            #         "varieties": varieties
            #     })

            seller_auth_id = Profile.objects.get(pk=seller_id).authority_id
            category_list = list(ProductCategory.objects.filter(
                is_hidden=False).values_list('id', 'name'))

            return render(request, 'product_form.html', {'product': product,
                                                        'images': image_array,
                                                        #  'varieties': p_varieties,
                                                        'category_list': category_list,
                                                        'seller_auth_id': seller_auth_id,
                                                        'media_url': s.MEDIA_URL})
        else:
            return render(request, '404.html')
    else:
        return render(request, '404.html')


def deleteOldVarieties(product):
    try:
        productVarieties = ProductVariety.objects.filter(product_id=product.id)
        for productVariety in productVarieties:
            productVarietySelections = ProductVarietySelection.objects.filter(
                product_variety_id=productVariety.id)
            for productVarietySelection in productVarietySelections:
                productJancodes = ProductJancode.objects.filter(
                    horizontal_id=productVarietySelection.id)
                for productJancode in productJancodes:
                    productJancode.is_hidden = True
                    productJancode.modified = datetime.datetime.now()
                    productJancode.save()
                productJancodes = ProductJancode.objects.filter(
                    vertical_id=productVarietySelection.id)
                for productJancode in productJancodes:
                    productJancode.is_hidden = True
                    productJancode.modified = datetime.datetime.now()
                    productJancode.save()

                productVarietySelection.is_hidden = True
                productVarietySelection.modified = datetime.datetime.now()
                productVarietySelection.save()

            productVariety.is_hidden = True
            productVariety.modified = datetime.datetime.now()
            productVariety.save()

    except Exception as e:
        print('deleteOldVarieties', e)



def hide_product(product_id):
    """
    Common Method to delete a product.
    """

    try:
        product = Product.objects.get(pk=product_id)
        product.is_hidden = 1
        product.modified = datetime.datetime.now()
        product.save()

        productImages = ProductImage.objects.filter(
            product_id=product.id, is_hidden=False)
        for productImage in productImages:
            image = Image.objects.get(pk=productImage.image_id)
            image.modified = datetime.datetime.now()
            image.is_hidden = True
            image.save()

            productImage.is_hidden = True
            productImage.modified = datetime.datetime.now()
            productImage.save()

        deleteOldVarieties(product)

        return True
    except Exception as e:
        print('hide_product', e)
        return False

    return True



@login_required
@csrf_exempt
def product_delete(request, product_id):
    """
    Method to delete a product.
    """

    if request.session['login_type'] == 'SELLER':
        result = hide_product(product_id)

        return redirect('/products/product_list/')
    else:
        return render(request, '404.html')



def updateProductVarieties(product, prdct_variety, varieties, old_varieties):
    """
    common Method to add or update a product variety.
    """

    try:
        if prdct_variety == 0:  # None
            obj = varieties[0]
            productJancode = ProductJancode.objects.get(pk=old_varieties[0]['id'])
            productJancode.jan_code = obj['jan_code']
            productJancode.stock = obj['stock']
            productJancode.save()
        else:
            if prdct_variety == 1:  # Horizontal or vertical
                for obj in varieties:
                    obj_varieties = obj['varieties']
                    found = False
                    for old in old_varieties:
                        if old['hor'] == obj_varieties[0]['selection'] or \
                            (old['jan_code'] != '' and old['jan_code'] == obj['jan_code']):
                            found = True
                            productJancode = ProductJancode.objects.get(pk=old['id'])
                            productJancode.jan_code = obj['jan_code']
                            productJancode.stock = obj['stock']
                            productJancode.save()
                            try:
                                productVarietySelection = ProductVarietySelection.objects.get(pk=productJancode.horizontal_id)
                                productVarietySelection.selection = obj_varieties[0]['selection']
                                productVarietySelection.save()

                                productVariety = ProductVariety.objects.get(pk=productVarietySelection.product_variety_id)
                                productVariety.name = obj_varieties[0]['name']
                                productVariety.save()
                            except:
                                pass
                            try:
                                productVarietySelection = ProductVarietySelection.objects.get(pk=productJancode.vertical_id)
                                productVarietySelection.selection = obj_varieties[0]['selection']
                                productVarietySelection.save()

                                productVariety = ProductVariety.objects.get(pk=productVarietySelection.product_variety_id)
                                productVariety.name = obj_varieties[0]['name']
                                productVariety.save()
                            except:
                                pass

                            old['id'] = ''
                            break
                    if not found: # new varient
                        productVariety = ProductVariety()
                        productVariety.name = obj_varieties[0]['name']
                        productVariety.vertical_and_horizontal = int(
                            obj_varieties[0]['vertical_and_horizontal'])
                        productVariety.product_id = product.id
                        productVariety.save()

                        productVarietySelection = ProductVarietySelection()
                        productVarietySelection.selection = obj_varieties[0]['selection']
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
                # delete extra varient
                for old in old_varieties:
                    if old['id'] != '':
                        productJancode = ProductJancode.objects.get(pk=old['id'])
                        productJancode.is_hidden = True
                        productJancode.save()

                        productVarietySelection = ProductVarietySelection.objects.get(pk=productJancode.horizontal_id)
                        productVarietySelection.is_hidden = True
                        productVarietySelection.save()

                        productVariety = ProductVariety.objects.get(pk=productVarietySelection.product_variety_id)
                        productVariety.is_hidden = True
                        productVariety.save()
            elif prdct_variety == 2:  # Horizontal and vertical
                for obj in varieties:
                    obj_varieties = obj['varieties']
                    found = False
                    for old in old_varieties:
                        if (old['hor'] == obj_varieties[0]['selection'] and \
                            old['ver'] == obj_varieties[1]['selection']) or \
                            (old['jan_code'] != '' and old['jan_code'] == obj['jan_code']):
                            found = True
                            productJancode = ProductJancode.objects.get(pk=old['id'])
                            productJancode.jan_code = obj['jan_code']
                            productJancode.stock = obj['stock']
                            productJancode.save()

                            try:
                                productVarietySelection1 = ProductVarietySelection.objects.get(pk=productJancode.horizontal_id)
                                productVarietySelection1.selection = obj_varieties[0]['selection']
                                productVarietySelection1.save()

                                productVariety = ProductVariety.objects.get(pk=productVarietySelection1.product_variety_id)
                                productVariety.name = obj_varieties[0]['name']
                                productVariety.save()
                            except:
                                pass
                            try:
                                productVarietySelection2 = ProductVarietySelection.objects.get(pk=productJancode.vertical_id)
                                productVarietySelection2.selection = obj_varieties[1]['selection']
                                productVarietySelection2.save()

                                productVariety = ProductVariety.objects.get(pk=productVarietySelection2.product_variety_id)
                                productVariety.name = obj_varieties[1]['name']
                                productVariety.save()
                            except:
                                pass

                            old['id'] = ''
                            break
                    if not found: # new varient
                        productVariety1 = ProductVariety()
                        productVariety1.name = obj_varieties[0]['name']
                        productVariety1.vertical_and_horizontal = int(
                            obj_varieties[0]['vertical_and_horizontal'])
                        productVariety1.product_id = product.id
                        productVariety1.save()

                        productVariety2 = ProductVariety()
                        productVariety2.name = obj_varieties[1]['name']
                        productVariety2.vertical_and_horizontal = int(
                            obj_varieties[1]['vertical_and_horizontal'])
                        productVariety2.product_id = product.id
                        productVariety2.save()

                        productVarietySelection1 = ProductVarietySelection()
                        productVarietySelection1.selection = obj_varieties[0]['selection']
                        productVarietySelection1.product_variety_id = productVariety1.id
                        productVarietySelection1.save()
                        productVarietySelection2 = ProductVarietySelection()
                        productVarietySelection2.selection = obj_varieties[1]['selection']
                        productVarietySelection2.product_variety_id = productVariety2.id
                        productVarietySelection2.save()

                        productJancode = ProductJancode()
                        productJancode.jan_code = obj['jan_code']
                        productJancode.stock = obj['stock']
                        productJancode.horizontal_id = productVarietySelection1.id
                        productJancode.vertical_id = productVarietySelection2.id
                        productJancode.save()
                # delete extra varient
                for old in old_varieties:
                    if old['id'] != '':
                        productJancode = ProductJancode.objects.get(pk=old['id'])
                        productJancode.is_hidden = True
                        productJancode.save()

                        productVarietySelection = ProductVarietySelection.objects.get(pk=productJancode.horizontal_id)
                        productVarietySelection.is_hidden = True
                        productVarietySelection.save()
                        productVariety = ProductVariety.objects.get(pk=productVarietySelection.product_variety_id)
                        productVariety.is_hidden = True
                        productVariety.save()

                        productVarietySelection = ProductVarietySelection.objects.get(pk=productJancode.vertical_id)
                        productVarietySelection.is_hidden = True
                        productVarietySelection.save()
                        productVariety = ProductVariety.objects.get(pk=productVarietySelection.product_variety_id)
                        productVariety.is_hidden = True
                        productVariety.save()
    except Exception as e:
        print('updateProductVarieties', e)

    return True



@csrf_exempt
def update_varieties(request):
    """
    ajax Method to add or update a product variety.
    """

    message = 'Error'
    if request.method == 'POST':
        try:
            if request.POST.get('product_id') and request.POST.get('product_id') != '':
                product_id = request.POST.get('product_id')
                product = Product.objects.get(pk=product_id)
                last_variety_type = product.variety

                # check if variety type changes
                # if so then delete 0ld data
                prdct_variety = int(request.POST.get('variety'))
                if last_variety_type != prdct_variety:
                    deleteOldVarieties(product)

                    # save new variety type
                    product.variety = prdct_variety
                    product.save()

                # save product new varieties
                varieties = json.loads(request.POST.get('varieties'))
                old_varieties = json.loads(request.POST.get('old_varieties'))
                if last_variety_type != prdct_variety:
                    old_varieties = []
                updateProductVarieties(product, prdct_variety, varieties, old_varieties)

                message = 'Success'
        except Exception as e:
            print('update_varieties', e)

    context = {'message': message}
    return HttpResponse(json.dumps(context), content_type="application/json")



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
                last_variety_type = product.variety
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

                # product image update
                if request.FILES.get('product_image0', False):
                    update_product_image(request.FILES.get('product_image0'), 1, product.id)
                if request.FILES.get('product_image1', False):
                    update_product_image(request.FILES.get('product_image1'), 2, product.id)
                if request.FILES.get('product_image2', False):
                    update_product_image(request.FILES.get('product_image2'), 3, product.id)
                if request.FILES.get('product_image3', False):
                    update_product_image(request.FILES.get('product_image3'), 4, product.id)
                if request.FILES.get('product_image4', False):
                    update_product_image(request.FILES.get('product_image4'), 5, product.id)

                # remove selected image
                deleted_images_list = json.loads(request.POST.get('image_delete'))
                if len(deleted_images_list):
                    delete_product_images(product.id, deleted_images_list)

                # check if variety type changes
                # if so then delete old data
                if last_variety_type != product.variety:
                    deleteOldVarieties(product)

                # save product new varieties
                varieties = json.loads(request.POST.get('varieties'))
                old_varieties = json.loads(request.POST.get('old_varieties'))
                if last_variety_type != product.variety:
                    old_varieties = []
                updateProductVarieties(product, product.variety, varieties, old_varieties)

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
                if request.FILES.get('product_image0', False):
                    save_product_image(request.FILES.get('product_image0'), 1, product.id)
                if request.FILES.get('product_image1', False):
                    save_product_image(request.FILES.get('product_image1'), 2, product.id)
                if request.FILES.get('product_image2', False):
                    save_product_image(request.FILES.get('product_image2'), 3, product.id)
                if request.FILES.get('product_image3', False):
                    save_product_image(request.FILES.get('product_image3'), 4, product.id)
                if request.FILES.get('product_image4', False):
                    save_product_image(request.FILES.get('product_image4'), 5, product.id)

                # save product varieties
                varieties = json.loads(request.POST.get('varieties'))
                saveNewVareities(product, varieties)


            message = 'Success'
        except Exception as e:
            print(e)

    context = {'message': message}
    return HttpResponse(json.dumps(context), content_type="application/json")



def saveNewVareities(product, varieties):
    """
    Common Method to add a product varieties.
    """

    try:
        if product.variety == 0:  # None
            obj = varieties[0]
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
            if product.variety == 1:  # Horizontal or vertical
                for obj in varieties:
                    obj_varieties = obj['varieties']
                    productVariety = ProductVariety()
                    productVariety.name = obj_varieties[0]['name']
                    productVariety.vertical_and_horizontal = int(
                        obj_varieties[0]['vertical_and_horizontal'])
                    productVariety.product_id = product.id
                    productVariety.save()

                    productVarietySelection = ProductVarietySelection()
                    productVarietySelection.selection = obj_varieties[0]['selection']
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
                for obj in varieties:
                    obj_varieties = obj['varieties']
                    productVariety1 = ProductVariety()
                    productVariety1.name = obj_varieties[0]['name']
                    productVariety1.vertical_and_horizontal = int(
                        obj_varieties[0]['vertical_and_horizontal'])
                    productVariety1.product_id = product.id
                    productVariety1.save()

                    productVariety2 = ProductVariety()
                    productVariety2.name = obj_varieties[1]['name']
                    productVariety2.vertical_and_horizontal = int(
                        obj_varieties[1]['vertical_and_horizontal'])
                    productVariety2.product_id = product.id
                    productVariety2.save()

                    productVarietySelection1 = ProductVarietySelection()
                    productVarietySelection1.selection = obj_varieties[0]['selection']
                    productVarietySelection1.product_variety_id = productVariety1.id
                    productVarietySelection1.save()
                    productVarietySelection2 = ProductVarietySelection()
                    productVarietySelection2.selection = obj_varieties[1]['selection']
                    productVarietySelection2.product_variety_id = productVariety2.id
                    productVarietySelection2.save()

                    productJancode = ProductJancode()
                    productJancode.jan_code = obj['jan_code']
                    productJancode.stock = obj['stock']
                    productJancode.horizontal_id = productVarietySelection1.id
                    productJancode.vertical_id = productVarietySelection2.id
                    productJancode.save()

    except Exception as e:
        print('saveNewVareities', e)



def delete_product_images(product_id, deleted_images_list):
    """
    Method to delete a product images.
    """

    try:
        # delete selected images
        for image_no in deleted_images_list:
            productImages = ProductImage.objects.filter(product_id=product_id, image_no=image_no, is_hidden=False)
            if productImages.exists():
                for productImage in productImages:
                    old_image = Image.objects.get(pk=productImage.image_id)
                    old_image.modified = datetime.datetime.now()
                    old_image.is_hidden = True
                    old_image.save()

                    productImage.is_hidden = True
                    productImage.modified = datetime.datetime.now()
                    productImage.save()

    except Exception as e:
        print('delete_product_images', e)

    return True


def update_product_image(image, image_no, product_id):
    """
    Method to update a product images.
    """

    try:
        # delete old images
        productImages = ProductImage.objects.filter(product_id=product_id, image_no=image_no, is_hidden=False)
        for productImage in productImages:
            old_image = Image.objects.get(pk=productImage.image_id)
            old_image.modified = datetime.datetime.now()
            old_image.is_hidden = True
            old_image.save()

            productImage.is_hidden = True
            productImage.modified = datetime.datetime.now()
            productImage.save()
        # save new one
        save_product_image(image, image_no, product_id)

    except Exception as e:
        print('update_product_image', e)

    return True


def save_product_image(image, image_no, product_id):
    """
    Method to add images of a product.
    """

    try:
        new_image = Image()
        new_image.image.save(image.name, image)
        new_image.save()

        productImage = ProductImage()
        productImage.image_id = new_image.id
        productImage.image_no = image_no
        productImage.product_id = product_id
        productImage.save()

    except Exception as e:
        print('save_product_image', e)

    return True

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
                    'category': str(product.category_id),
                    'target': str(product.target),
                    'price': str(product.price),
                    'store_price': str(product.store_price),
                    'shipping_fee': str(product.shipping_fee),
                    'opened_date': product.opened_date.strftime('%Y-%m-%d') if product.opened_date else '',
                    'is_opened': '1' if product.is_opened else '0',
                    'is_used': '1' if product.is_used else '0',
                    'is_draft': '1' if product.is_draft else '0',
                    'variety': str(product.variety),
                }
                image_array = []
                productImages = ProductImage.objects.filter(
                    product_id=product.id, is_hidden=False).order_by('image_no').exclude(image_no__isnull=True)
                for productImage in productImages:
                    image_array.append({
                        "url": productImage.image.image.url,
                        "image_no": str(productImage.image_no)
                    })

                context['images'] = image_array

                p_varieties = []
                jancode_ids = get_products_jancodes(product.id, type='id')
                for jan_id in jancode_ids:
                    varieties = []
                    productJancode = ProductJancode.objects.get(pk=jan_id)
                    if productJancode.horizontal_id:
                        productVarietySelection = ProductVarietySelection.objects.get(
                            pk=productJancode.horizontal_id)
                        productVariety = ProductVariety.objects.get(
                            pk=productVarietySelection.product_variety_id)
                        varieties.append({
                            "name": str(productVariety.name),
                            "selection": str(productVarietySelection.selection),
                            "vertical_and_horizontal": str(productVariety.vertical_and_horizontal),
                        })
                    if productJancode.vertical_id:
                        productVarietySelection = ProductVarietySelection.objects.get(
                            pk=productJancode.vertical_id)
                        productVariety = ProductVariety.objects.get(
                            pk=productVarietySelection.product_variety_id)
                        varieties.append({
                            "name": str(productVariety.name),
                            "selection": str(productVarietySelection.selection),
                            "vertical_and_horizontal": str(productVariety.vertical_and_horizontal),
                        })
                    p_varieties.append({
                        "id": str(productJancode.id),
                        "jan_code": str(productJancode.jan_code),
                        "stock": str(productJancode.stock),
                        "varieties": varieties
                    })
                context['varieties'] = p_varieties

        except Exception as e:
            print(e)

    return HttpResponse(json.dumps(context), content_type="application/json")


@csrf_exempt
def delete_product(request):
    """
    ajax Method to delete a product.
    """

    message = 'Error'
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        result = hide_product(product_id)
        if result:
            message = 'Success'

    context = {'message': message}
    return HttpResponse(json.dumps(context), content_type="application/json")


@csrf_exempt
def update_product_from_list(request):
    """
    ajax Method to update a product's price & stock from list table.
    """

    message = 'Error'
    if request.method == 'POST':
        product = eval(request.POST.get('product'))
        new_price = request.POST.get('new_price')
        new_stock = request.POST.get('new_stock')
        if new_price != '':
            try:
                print(product, new_price)
                s_product = Product.objects.get(id=product['id'])
                s_product.price = int(new_price)
                if s_product.user.authority_id == AUTHORITY_TYPE['MASTER']:
                    s_product.store_price = s_product.price - int(0.3 * float(s_product.price))
                else:
                    s_product.store_price = s_product.price - int(0.2 * float(s_product.price))
                s_product.modified = datetime.datetime.now()
                s_product.save()

                message = 'Success'
            except Exception as e:
                print(e)
        if new_stock != '' and int(new_stock) > 0:
            try:
                j_product = ProductJancode.objects.get(id=product['jan_id'])
                j_product.stock = int(new_stock)
                j_product.modified = datetime.datetime.now()
                j_product.save()

                message = 'Success'
            except Exception as e:
                print(e)

    context = {'message': message}
    return HttpResponse(json.dumps(context), content_type="application/json")


@login_required
def export_product_list_as_csv(request):
    """
    Method to get product list as CSV.
    """

    profile_id = request.session['login_profile_id']
    product_list = Product.objects.filter(is_hidden=False, user_id=profile_id).order_by('name')
    filter_array = eval(request.POST.get('param0'))
    if len(filter_array):
        if 1 not in filter_array:
            product_list = product_list.exclude(is_opened=True)
        if 2 not in filter_array:
            product_list = product_list.exclude(is_opened=False)
        if 3 not in filter_array:
            product_list = product_list.exclude(is_draft=True)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="ProductList.csv"'
    writer = csv.writer(response)
    writer.writerow(['#', 'product_name', 'jan_code', 'varieties', 'stock', 'price', 'opened_date'])

    i = 0
    for field in product_list:
        jancode_ids = get_products_jancodes(field.id, type='id')
        productJancodes = ProductJancode.objects.filter(id__in=jancode_ids)
        for p_jan in productJancodes:
            veries = get_jan_varieties(p_jan)
            very_str = ''
            for item in veries:
                if item['name']:
                    very_str += item['name'] + ' : ' + item['selection'] + ','
            if len(very_str):
                very_str = very_str[:-1]
            else:
                language = translation.get_language()
                if language == 'ja':
                    very_str = '無し'
                else:
                    very_str = 'None'
            i = i + 1
            writer.writerow([str(i), field.name, str(p_jan.jan_code), very_str,
                            str(p_jan.stock), intcomma("%.0f" % field.price),
                            field.opened_date.strftime("%Y-%m-%d") if field.opened_date else ''])


    return response
