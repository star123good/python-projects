# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.contrib.auth.models import User


class UserType(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
    
    class Meta:
        abstract = True

class Customer(UserType):
    pass 

class Partner(UserType):
    pass 


class Package(models.Model):
    currencycode = models.CharField(
        max_length=3, null=False, blank=False, default="")
    currencysymbol = models.CharField(
        max_length=16, null=False, blank=False, default="")
    zerodecimal = models.BooleanField(default=False)
    packagetype = models.CharField(
        max_length=32, null=False, blank=False, default="")
    packagename = models.CharField(
        max_length=256, null=False, blank=False, default="")
    planname = models.CharField(
        max_length=256, null=False, blank=False, default="")
    planid = models.CharField(
        max_length=256, null=False, blank=False, default="")
    packagediscount = models.IntegerField(default=0)
    intervalcount = models.IntegerField(default=0)
    price = models.BigIntegerField(default=0)
    quota = models.BigIntegerField(default=0)
    priceoverquota = models.IntegerField(default=0)


class PartnerCredential(models.Model):
    partner = models.ForeignKey('Partner', on_delete=models.CASCADE)
    api_key = models.CharField(
        max_length=128, null=False, blank=False, default="")
    api_secret = models.CharField(
        max_length=128, null=False, blank=False, default="")
    description = models.CharField(max_length=1024, null=True, blank=True)


class CustomerCredential(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    api_key = models.CharField(
        max_length=128, null=False, blank=False, default="")
    api_secret = models.CharField(
        max_length=128, null=False, blank=False, default="")
    description = models.CharField(max_length=1024, null=True, blank=True)


class AdministratorCredential(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    api_key = models.CharField(
        max_length=128, null=False, blank=False, default="")
    api_secret = models.CharField(
        max_length=128, null=False, blank=False, default="")
    description = models.CharField(max_length=1024, null=True, blank=True)


class FileType(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    filehash = models.CharField(
        max_length=128, null=False, blank=False, default="")
    size_unoptimized = models.IntegerField(default=0)
    size_optimized = models.IntegerField(default=0)
    fileurl = models.CharField(
        max_length=2000, null=False, blank=False, default="")
    filepath = models.CharField(
        max_length=4096, null=False, blank=False, default="")


class UnoptimizedFile(models.Model):
    customer = models.BigIntegerField(default=0)
    filehash = models.CharField(
        max_length=128, null=False, blank=False, default="")
    size_unoptimized = models.IntegerField(default=0)
    fileurl = models.CharField(
        max_length=2000, null=False, blank=False, default="")
    filepath = models.CharField(
        max_length=4096, null=False, blank=False, default="")
