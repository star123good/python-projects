from django.shortcuts import render
from rest_framework import serializers, viewsets, routers
from . import stripeserializer as stripe_serializer
from djstripe import models as djstripe_model

# Create your views here.

# ViewSets define the view behavior.
class AccountViewSet(viewsets.ModelViewSet):
    queryset = djstripe_model.Account.objects.all()
    serializer_class = stripe_serializer.AccountSerializer

class ChargeViewSet(viewsets.ModelViewSet):
    queryset = djstripe_model.Charge.objects.all()
    serializer_class = stripe_serializer.AccountSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = djstripe_model.Customer.objects.all()
    serializer_class = stripe_serializer.CustomerSerializer

class PlanViewSet(viewsets.ModelViewSet):
    queryset = djstripe_model.Plan.objects.all()
    serializer_class = stripe_serializer.PlanSerializer

class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = djstripe_model.Subscription.objects.all()
    serializer_class = stripe_serializer.SubscriptionSerializer
    
