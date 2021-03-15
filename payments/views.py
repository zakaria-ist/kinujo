import json
import stripe
# import date
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView

# Create your views here.

class PayView(TemplateView):
    template_name = 'pay.html'

class SuccessView(TemplateView):
    template_name = 'success.html'

class CancelledView(TemplateView):
    template_name = 'cancelled.html'

# def post(userId, products, address, tax, checkoutSessionId):
#         try:

#             sellers = []
#             profile = Profile.objects.get(id=userId, is_hidden=False)
#             # tax = TaxRate.objects.get(id=request.data['tax'], is_hidden=False)
#             tax = TaxRate.objects.get(id=tax, is_hidden=False)
#             # token_id = token.id
#             customer_id = None

#             ids = []
#             quantities = {}
#             varieties = {}

#             # for product in request.data['products']:
#             for product in products:
#                 quantities['item_' + str(product['product_id'])] = product['quantity']
#                 varieties['item_' + str(product['product_id'])] = product['varietyId']
#                 ids.append(product['product_id'])

#             products = Product.objects.filter(id__in=ids)
#             # address = Address.objects.get(id=request.data['address'])
#             address = Address.objects.get(id=address)

#             groupProducts = {}
#             orderIds = []

#             if products and profile and address:
#                 profileSerializer = ProfileSerializer(profile, context=getContext())
#                 productSerializer = ProductSerializer(products, many=True, context=getContext())
#                 addressSerializer = AddressSerializer(address, context=getContext())

#                 amount = total_amount = total_tax = total_shipping_fee = 0
#                 seller = None
#                 product_name = ''
#                 one_product = ''

#                 for product in productSerializer.data:
#                     seller = Profile.objects.get(pk=product['user']['id'])
#                     one_product = product
#                     product_name = product['name']
#                     quantity = quantities['item_' + str(product['id'])]
#                     if profileSerializer.data['is_seller']:
#                         amount = int(float(amount) + (float(product['store_price']) * float(quantity)))
#                     else:
#                         amount = int(float(amount) + (float(product['price']) * float(quantity)))
#                     total_tax = int(total_tax) + int(float(amount) * float(tax.tax_rate))
#                     total_shipping_fee = int(float(total_shipping_fee) + float(product['shipping_fee']))

                
#                 total_amount = int(amount) + int(total_shipping_fee)

#                 address2 = addressSerializer.data['address2']
#                 if address2 is None:
#                     address2 = "no_address_2"

#                 order = {
#                     'amount' : amount,
#                     'tax': total_tax,
#                     'shipping_fee': total_shipping_fee,
#                     'shipped_date': None,
#                     'total_amount': total_amount + total_tax,
#                     'name': addressSerializer.data['name'],
#                     'zip1': addressSerializer.data['zip1'],
#                     'tel_code': addressSerializer.data['tel_code'],
#                     'address1': addressSerializer.data['address1'],
#                     'address2': address2,
#                     'tel': addressSerializer.data['tel'],
#                     'is_hidden': 0,
#                     'prefecture': addressSerializer.data['prefecture']['url'],
#                     'seller': one_product['user']['url'],
#                     'purchaser' : profileSerializer.data['url'],
#                     'status' : 1
#                 }
#                 orderSerializer = InsertOrderSerializer(data=order, context=getContext())
#                 if orderSerializer.is_valid():
#                     newOrder = orderSerializer.save()
#                     shop_name = ""
#                     if seller.shop_name:
#                         shop_name = seller.shop_name
#                     elif seller.real_name:
#                         shop_name = seller.real_name
#                     elif seller.nickname:
#                         shop_name = seller.nickname

#                     orderReceipt = {
#                         'is_copy' : 0,
#                         'to_name' : addressSerializer.data['name'],
#                         'amount' : total_amount,
#                         'output_date' : date.today(),
#                         'order_date' : date.today(),
#                         'product_name' : product_name,
#                         'shop_name' : shop_name,
#                         'address' : addressSerializer.data['address1'],
#                         'order' : orderSerializer.data['url'],
#                         'payment' : checkoutSessionId
#                     }
#                     orderReceiptSerializer = OrderReceiptSerializer(data=orderReceipt, context=getContext())
#                     if orderReceiptSerializer.is_valid():
#                         orderReceiptSerializer.save()

#                     kinujo_product = if_kinujo_product(seller.id)
#                     for product in productSerializer.data:
#                         quantity = quantities['item_' + str(product['id'])]
#                         price = 0
#                         groupTotal = 0
#                         groupShippingFee = float(product['shipping_fee'])

#                         if profileSerializer.data['is_seller']:
#                             price= float(product['store_price'])
#                             groupTotal = int(float(product['store_price']) * float(quantity))
#                         else:
#                             price= float(product['price'])
#                             groupTotal = int(float(product['price']) * float(quantity))
#                         groupTax = int(float(groupTotal) * float(tax.tax_rate))

#                         varietyId = varieties['item_' + str(product['id'])]

#                         variety = None
#                         variety = ProductJancode.objects.get(id=varietyId)
#                         varietySerializer = ProductJancodeSerializer(variety, context=getContext())
#                         variety = varietySerializer.data['url']

#                         orderIds.append(orderSerializer.data['id'])

#                         orderProduct = {
#                             'quantity':  quantity,
#                             'unit_price' : int(price),
#                             'total_price' : groupTotal,
#                             'tax': groupTax,
#                             'total_amount': groupTotal + groupTax,
#                             'order': orderSerializer.data['url'],
#                             'product_jan_code': variety
#                         }
#                         orderProductSerializer = InsertOrderProductSerializer(data=orderProduct, context=getContext())
#                         if orderProductSerializer.is_valid():
#                             orderProductSerializer.save()

#                             productJancode = ProductJancode.objects.get(id=varietyId)
#                             if productJancode:
#                                 productJancode.stock = int(productJancode.stock) - int(quantity)
#                                 productJancode.save()

#                             errors = calculateCommission(kinujo_product, float(product['price']), orderProductSerializer.data['url'], 
#                                         profileSerializer.data['id'], groupShippingFee, groupTotal, seller)

#                         if product['user']['email']:
#                             send_mail(
#                                 '[KINUJOからのお知らせ」出品中の商品が購入されました',
#                                 'いつもKINUJOをご利用いただきありがとうございます。' + "<br><br>" +
#                                 '出品中の下記の商品が購入されまUた。' +  "<br>" +
#                                 '商品の発送をお願いいたします。' + "<br><br>" +
#                                 '商品情報' + "<br>" +
#                                 'オーダーID:' + str(orderSerializer.data['id']) + "<br>" +
#                                 '商品名:' + product['name'] + "<br>" +
#                                 '商品価格:' + str(float(groupTotal)) + "<br>" +
#                                 '購入者様:' + addressSerializer.data['name'] + "<br>" + "<br>" +
#                                 '発送を終えたら' + "<br>" +
#                                 '管理サイトから注文の状態を発送完了に変更し、発送日とお問い合わせ番号を入力Uて更新Uてください。' + "<br>" +
#                                 '発送した日、配送方法やお問い合わせ番号をチャットでお伝えいただくと、購入者様も喜ばれます。' + "<br><br>" +
#                                 "お問い合わせは、アプリ内のチャットをご利用＜ださい。",
#                                 'support@kinujo.app',
#                                 [product['user']['email']],
#                                 fail_silently=False,
#                             )

#                         sellers.append(product['user']['id'])
                
            

#         except Exception as e:
#             pass


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        domain_url = request.build_absolute_uri('/').strip("/")
        body = json.loads(request.body)
        total = body['amount']
        # products = body['products']
        # address = body['address']
        # tax = body['tax']
        # userId = body['userId']
        # stripe.api_key = 'sk_test_51INa46G0snPTYlWjdSzH5xxz70p7FZwcWbO37zos9U6jg1WXOMeNCtPrbOA3BXZWavBz7N67wLiYP5ZSQPp2QonF00VbEj1Gfc'
        stripe.api_key = 'sk_test_51HKjPHIvJqFxVlDAV0kJVoq8oXNuwUukI6r6rjaUnjQdJJwFRUpi04AC2m4LmTV7NQEpICIa2vgWr982UVkY8Qyr00TJuir4I7'
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + '/payments/success?sc_checkout=success&sc_sid={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + '/payments/cancelled?sc_checkout=cancel',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'jpy',
                        'product_data': {
                            'name': 'Kinujo',
                        },
                        'unit_amount': total,
                    },
                    'quantity': 1,
                }],
            )
            content = {'sessionId': checkout_session['id']}
            json_content = json.dumps(content, ensure_ascii=False)
            return HttpResponse(json_content, content_type='application/json')
        except Exception as e:
            content = {'error': str(e)}
            json_content = json.dumps(content, ensure_ascii=False)
            return HttpResponse(json_content, content_type='application/json')

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = 'sk_test_51HKjPHIvJqFxVlDAV0kJVoq8oXNuwUukI6r6rjaUnjQdJJwFRUpi04AC2m4LmTV7NQEpICIa2vgWr982UVkY8Qyr00TJuir4I7'
    # endpoint_secret = 'whsec_ZAuQoadHEP4xL2w37AmaBSgnQDj5EUVr'
    endpoint_secret = 'whsec_9EgKdzB2A0ydf87EBbJrpQBMeiDAwE0V'
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        if session.payment_status == "paid":
            # Fulfill the purchase
            print("Payment was successful.")
            # TODO: run some custom code here
    elif event['type'] == 'checkout.session.async_payment_succeeded':
        session = event['data']['object']
        if session.payment_status == "paid":
            # Fulfill the purchase
            print("Payment was successful.")
            # TODO: run some custom code here
    elif event['type'] == 'checkout.session.async_payment_failed':
        # TODO: run some custom code here
        print('Failed')

    return HttpResponse(status=200)