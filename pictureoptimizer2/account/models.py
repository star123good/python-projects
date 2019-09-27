# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.models import User


# Create your models here.
#
class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ispartner = models.BooleanField(default=False)
    partnerid = models.BigIntegerField(default=1)
    phone = models.CharField(max_length=25, null=True, blank=True)
    company = models.CharField(max_length=255, null=True, blank=True)
    website = models.CharField(max_length=255, null=True, blank=True)
    fax = models.CharField(max_length=255, null=True, blank=True)
    subscription_id = models.CharField(max_length=255, null=True, blank=True)
    min_subscipitions = models.IntegerField(default=0)
    max_subscipitions = models.IntegerField(default=0)
    about_company = models.CharField(max_length=4096, null=True, blank=True)
    customer_id = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.first_name


class Subscription(models.Model):
    # id = models.BigIntegerField(primary_key=True)
    customer_id = models.BigIntegerField(default=1)
    packageid = models.BigIntegerField(default=0)
    partnerid = models.BigIntegerField(default=0)
    billing = models.CharField(max_length=64, null=False, blank=False, default="")
    cancel_at_period_end = models.BooleanField(default=False)
    canceled_at = models.DateTimeField()
    current_period_end = models.DateTimeField()
    current_period_start = models.DateTimeField()
    customer = models.CharField(max_length=64, null=False, blank=False, default="")
    subscription_id = models.CharField(max_length=64, null=False, blank=False, default="")
    subscription_created = models.DateTimeField()
    subscription_item_id = models.CharField(max_length=64, null=False, blank=False, default="")
    plan_amount = models.IntegerField(default=0)
    plan_created = models.DateTimeField()
    plan_currency = models.CharField(max_length=3, null=False, blank=False, default="")
    plan_id = models.CharField(max_length=256, null=False, blank=False, default="")
    plan_interval = models.CharField(max_length=8, null=False, blank=False, default="")
    plan_interval_count = models.IntegerField()
    plan_livemode = models.BooleanField()
    plan_name = models.CharField(max_length=256, null=False, blank=False, default="")
    quantity = models.IntegerField(default=0)
    object_type = models.CharField(max_length=32, null=False, blank=False, default="")
    total_count = models.IntegerField(default=0)
    start = models.DateTimeField()
    status = models.CharField(max_length=128, null=False, blank=False, default="")

    def __str__(self):
        return self.billing


class Package(models.Model):
    # id = models.BigIntegerField(primary_key=True)
    currencycode = models.CharField(max_length=3, null=False, blank=False, default="")
    currencysymbol = models.CharField(max_length=16, null=False, blank=False, default="")
    zerodecimal = models.BooleanField(default=False)
    packagetype = models.CharField(max_length=32, null=False, blank=False, default="")
    packagename = models.CharField(max_length=256, null=False, blank=False, default="")
    planname = models.CharField(max_length=256, null=False, blank=False, default="")
    planid = models.CharField(max_length=256, null=False, blank=False, default="")
    packagediscount = models.IntegerField(default=0)
    intervalcount = models.IntegerField(default=0)
    price = models.BigIntegerField(default=0)
    quota = models.BigIntegerField(default=0)
    priceoverquota = models.IntegerField(default=0)


class PartnerCredential(models.Model):
    # id = models.BigIntegerField(primary_key=True)
    partnerid = models.BigIntegerField(default=1)
    api_key = models.CharField(max_length=128, null=False, blank=False, default="")
    api_secret = models.CharField(max_length=128, null=False, blank=False, default="")
    description = models.CharField(max_length=1024, null=True, blank=True)


class CustomerCredential(models.Model):
    # id = models.BigIntegerField(primary_key=True)
    customerid = models.BigIntegerField(default=1)
    api_key = models.CharField(max_length=128, null=False, blank=False, default="")
    api_secret = models.CharField(max_length=128, null=False, blank=False, default="")
    description = models.CharField(max_length=1024, null=True, blank=True)


class AdministratorCredential(models.Model):
    # id = models.BigIntegerField(primary_key=True)
    customerid = models.BigIntegerField(default=1)
    api_key = models.CharField(max_length=128, null=False, blank=False, default="")
    api_secret = models.CharField(max_length=128, null=False, blank=False, default="")
    description = models.CharField(max_length=1024, null=True, blank=True)


class OptimizedFile(models.Model):
    # id = models.BigIntegerField(primary_key=True)
    customerid = models.BigIntegerField(default=0)
    filehash = models.CharField(max_length=128, null=False, blank=False, default="")
    size_unoptimized = models.IntegerField(default=0)
    size_optimized = models.IntegerField(default=0)
    fileurl = models.CharField(max_length=2000, null=False, blank=False, default="")
    filepath = models.CharField(max_length=4096, null=False, blank=False, default="")


class UnoptimizedFile(models.Model):
    # id = models.BigIntegerField(primary_key=True)
    customerid = models.BigIntegerField(default=0)
    filehash = models.CharField(max_length=128, null=False, blank=False, default="")
    size_unoptimized = models.IntegerField(default=0)
    fileurl = models.CharField(max_length=2000, null=False, blank=False, default="")
    filepath = models.CharField(max_length=4096, null=False, blank=False, default="")


from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserData.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userdata.save()
