from rest_framework import serializers, viewsets, routers
from djstripe import models as stripe_model


# Serializers define the API representation.
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = stripe_model.Account
        fields = '__all__'

class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = stripe_model.Charge
        fields = '__all__'

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = stripe_model.Customer
        fields = '__all__'

class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = stripe_model.Plan
        fields = '__all__'

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = stripe_model.Subscription
        fields = '__all__'