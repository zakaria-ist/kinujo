import json
import stripe
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

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        domain_url = request.build_absolute_uri('/').strip("/")
        print('domain_url', domain_url)
        stripe.api_key = 'sk_test_51INa46G0snPTYlWjdSzH5xxz70p7FZwcWbO37zos9U6jg1WXOMeNCtPrbOA3BXZWavBz7N67wLiYP5ZSQPp2QonF00VbEj1Gfc'
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
                success_url=domain_url + '/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + '/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[{
                    'price_data': {
                        'currency': 'jpy',
                        'product_data': {
                        'name': 'T-shirt',
                        },
                        'unit_amount': 2000,
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
    stripe.api_key = 'sk_test_51INa46G0snPTYlWjdSzH5xxz70p7FZwcWbO37zos9U6jg1WXOMeNCtPrbOA3BXZWavBz7N67wLiYP5ZSQPp2QonF00VbEj1Gfc'
    endpoint_secret = 'whsec_ZAuQoadHEP4xL2w37AmaBSgnQDj5EUVr'
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
        print("Payment was successful.")
        # TODO: run some custom code here

    return HttpResponse(status=200)