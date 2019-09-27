from django.db import models

# Create your models here.


class Subscription(models.Model):
    packageid = models.BigIntegerField(default=0)
    partnerid = models.BigIntegerField(default=0)
    billing = models.CharField(
        max_length=64, null=False, blank=False, default="")
    cancel_at_period_end = models.BooleanField(default=False)
    canceled_at = models.DateTimeField()
    current_period_end = models.DateTimeField()
    current_period_start = models.DateTimeField()
    customer = models.CharField(
        max_length=64, null=False, blank=False, default="")
    subscription_id = models.CharField(
        max_length=64, null=False, blank=False, default="")
    subscription_created = models.DateTimeField()
    subscription_item_id = models.CharField(
        max_length=64, null=False, blank=False, default="")
    plan_amount = models.IntegerField(default=0)
    plan_created = models.DateTimeField()
    plan_currency = models.CharField(
        max_length=3, null=False, blank=False, default="")
    plan_id = models.CharField(
        max_length=256, null=False, blank=False, default="")
    plan_interval = models.CharField(
        max_length=8, null=False, blank=False, default="")
    plan_interval_count = models.IntegerField()
    plan_livemode = models.BooleanField()
    plan_name = models.CharField(
        max_length=256, null=False, blank=False, default="")
    quantity = models.IntegerField(default=0)
    object_type = models.CharField(
        max_length=32, null=False, blank=False, default="")
    total_count = models.IntegerField(default=0)
    start = models.DateTimeField()
    status = models.CharField(
        max_length=128, null=False, blank=False, default="")

    def __str__(self):
        return self.billing

    # customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    # packageid = models.BigIntegerField(default=0)
    # partnerid = models.BigIntegerField(default=0)
    # billing = models.CharField(
    #     max_length=64, null=False, blank=False, default="")
    # cancel_at_period_end = models.BooleanField(default=False)
    # canceled_at = models.DateTimeField()
    # current_period_end = models.DateTimeField()
    # current_period_start = models.DateTimeField()
    # customer = models.CharField(
    #     max_length=64, null=False, blank=False, default="")
    # subscription_id = models.CharField(
    #     max_length=64, null=False, blank=False, default="")
    # subscription_created = models.DateTimeField()
    # subscription_item_id = models.CharField(
    #     max_length=64, null=False, blank=False, default="")
    # plan_amount = models.IntegerField(default=0)
    # plan_created = models.DateTimeField()
    # plan_currency = models.CharField(
    #     max_length=3, null=False, blank=False, default="")
    # plan_id = models.CharField(
    #     max_length=256, null=False, blank=False, default="")
    # plan_interval = models.CharField(
    #     max_length=8, null=False, blank=False, default="")
    # plan_interval_count = models.IntegerField()
    # plan_livemode = models.BooleanField()
    # plan_name = models.CharField(
    #     max_length=256, null=False, blank=False, default="")
    # quantity = models.IntegerField(default=0)
    # object_type = models.CharField(
    #     max_length=32, null=False, blank=False, default="")
    # total_count = models.IntegerField(default=0)
    # start = models.DateTimeField()
    # status = models.CharField(
    #     max_length=128, null=False, blank=False, default="")

    # def __str__(self):
    #     return self.billing
