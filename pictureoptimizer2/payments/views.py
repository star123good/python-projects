# payments/views.py
import stripe  # new
from django.conf import settings
from django.views.generic.base import TemplateView
from django.shortcuts import render  # new
from django.http import HttpResponseRedirect
import requests
from datetime import datetime

from account.models import Package, Subscription

stripe.api_key = settings.STRIPE_SECRET_KEY  # new


class PaymentPageView(TemplateView):
    template_name = 'payment.html'

    def get_context_data(self, **kwargs):
        context = super(PaymentPageView, self).get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request):  # new
    if request.method == 'POST':
        print(request.POST)
        charge = stripe.Charge.create(
            amount=500,
            currency='usd',
            description='A Django charge',
            source=request.POST['stripeToken']
        )
        return render(request, 'charge.html')


def SubscriptionView(request):  # new
    if request.method == 'POST':
        # for key, value in request.POST.items():
        #   print('Key: %s' % (key) )
        #   print('Value %s' % (value) )
        # Input your stripe api key here
        # stripe.api_key = "sk_test_xvZ0tohEbZKWmEyLbC4aH2SV"

        try:
            card_exp_date = request.POST['cardExpiry'].split("/")
            ResponseToken = stripe.Token.create(
                card={
                    # Here values from your form are passed and a token is created in the ResponseToken variable
                    "number": request.POST['cardNumber'],
                    "exp_month": card_exp_date[0],
                    "exp_year": card_exp_date[1],
                    "cvc": request.POST['cardCVC']
                },
            )
            token = ResponseToken.id  # generated token

            user_emain = request.POST['email']

            new_customer = stripe.Customer.create(  # new customer is created //Here you have to provide a mail address of the customer
                source=token,
                email=user_emain,
            )
            csid = new_customer['id']  # generated customer id

            if request.POST['payment_type'] == 'BASIC':
                plan_ids = settings.PLAIN_ID_BASIC
                price = 27
            elif request.POST['payment_type'] == 'PRO':
                plan_ids = settings.PLAIN_ID_PRO
                price = 74
            elif request.POST['payment_type'] == 'UNLIMITED':
                plan_ids = settings.PLAIN_ID_UNLIMITED
                price = 140
            else:
                plan_ids = settings.PLAIN_ID_STARTER
                price = 9
                
            if request.POST['payment_interval'] == 'ThreeMonth':
                plan_id = plan_ids[1]
            elif request.POST['payment_interval'] == 'SixMonth':
                plan_id = plan_ids[2]
            elif request.POST['payment_interval'] == 'Yearly':
                plan_id = plan_ids[3]
            else:
                plan_id = plan_ids[0]

            subscription = stripe.Subscription.create(  # Customer will now subscribe to the following plan
                customer=csid,
                # here you have to set the plan of the customer
                items=[{'plan': plan_id}],
            )

            package = Package(currencycode='USD',currencysymbol='$',planid=request.POST['payment_type'],price=price)
            package.save()

            subscription_model = Subscription(customer_id=request.user.id,packageid=package.id,plan_id=request.POST['payment_type'],quantity=price,
                                canceled_at=datetime.now(),current_period_end=datetime.now(),subscription_created=datetime.now(),
                                plan_created=datetime.now(),current_period_start=datetime.now(),start=datetime.now(),
                                plan_interval_count=0,plan_livemode=True)
            subscription_model.save()

            return render(request, 'subscription_success.html')
        except Exception as e:
            print(e)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
