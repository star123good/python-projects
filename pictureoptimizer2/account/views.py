# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from pprint import pprint
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
from django.conf import settings
# Create your views here.
from datetime import datetime

import uuid

from . import models

@login_required
def dashboard(request):
    # return render(request, 'account_overview.html')
    return account_overview(request)


@login_required
def account_overview(request):
    subscription = Subscription.objects.latest('id')
    package = Package.objects.get(id=subscription.packageid)
    optimized_files = OptimizedFile.objects.filter(customerid=request.user.id)
    unoptimized_files = UnoptimizedFile.objects.filter(customerid=request.user.id)

    context = model_to_dict(package)

    context['max_upload_size'] = settings.MAX_UPLOAD_SIZE
    context['paln_level'] = context['currencysymbol'] + str(context['price']) + '/month' if context['price'] > 0 else 'FREE'

    context['total_file_size'] = 0
    context['optimized_file_size'] = 0
    context['file_counter'] = 0
    for optimized_file in optimized_files:
        context['total_file_size'] += optimized_file.size_unoptimized
        context['optimized_file_size'] += optimized_file.size_optimized
        context['file_counter'] += 1
    for unoptimized_file in unoptimized_files:
        context['total_file_size'] += unoptimized_file.size_unoptimized
        context['optimized_file_size'] += unoptimized_file.size_unoptimized
        context['file_counter'] += 1
    context['optimized_percent'] = round(100 * context['optimized_file_size'] / context['total_file_size']) if context['total_file_size'] > 0 else 0

    return render(request, 'account_overview.html', context)


@login_required
def api_dashboard(request, command_type=''):
    context = {}
    api_key = api_secret = ''

    if command_type == 'generate':
        api_key = str(uuid.uuid4()).replace('-', '')
        api_secret = str(uuid.uuid4()).replace('-', '')
        customer_credential = CustomerCredential(customerid=request.user.id,api_key=api_key, api_secret=api_secret)
        customer_credential.save()
    elif command_type == 'remove':
        CustomerCredential.objects.filter(customerid=request.user.id).delete()
    else:
        customer_credential = CustomerCredential.objects.filter(customerid=request.user.id)
        if customer_credential.exists():
            api_key = customer_credential.latest('id').api_key
            api_secret = customer_credential.latest('id').api_secret
        
    context['api_key'] = api_key
    context['api_secret'] = api_secret
    context['btn_generate'] = 'Generate' if api_key == '' else 'Re-Generate'

    return render(request, 'api_dashboard.html', context)


@login_required
def web_interface_pro(request):
    return render(request, 'file_uploader.html')


@login_required
def delivered_webhooks(request):
    return render(request, 'delivered_webhooks.html')


@login_required
def plans_and_billing(request):
    return render(request, 'plans_and_billing.html')


@login_required
def redeem_coupon(request):
    return render(request, 'redeem_coupon.html')


@login_required
def plans_info(request):
    return render(request, 'plans_info.html')


@login_required
def file_uploader(request):
    return render(request, 'file_uploader.html')


@login_required
def url_paster(request):
    return render(request, 'url_paster.html')


@login_required
def payment(request):
    return render(request, 'payment.html')


@login_required
def adding_billing_info(request, payment_type='STARTER'):
    context = {
        'payment_type' : payment_type, 
        'user_email' : request.user.email
    }
    return render(request, 'adding_billing_info.html', context)


@login_required
def page_cruncher(request):
    print request.POST
    return render(request, 'page_cruncher.html')


def web_interface_pro_upload_files(request):
    print request.POST
    print request.FILES
    print "Here"
    data = dict()
    data['name'] = 'randomname.png'
    data['originalSize'] = '12'
    data['modSize'] = '87'
    data['savings'] = '542'
    data['perSaving'] = '09'
    data['downloadImageUrl'] = 'http://via.placeholder.com/350x150'
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def page_cruncher_uploader_ajax(request):
    print request.POST
    data = dict()
    data['name'] = 'randomname.png'
    data['originalSize'] = '12'
    data['modSize'] = '87'
    data['savings'] = '542'
    data['perSaving'] = '09'
    data['downloadImageUrl'] = 'http://via.placeholder.com/350x150'
    return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def url_paster_uploader_ajax(request):
    print request.POST
    data = dict()
    data['name'] = 'randomname.png'
    data['originalSize'] = '12'
    data['modSize'] = '87'
    data['savings'] = '542'
    data['perSaving'] = '09'
    data['downloadImageUrl'] = 'http://via.placeholder.com/350x150'
    return HttpResponse(json.dumps(data), content_type='application/json')


from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from datetime import datetime
from .models import *


def registration(request):
    rg = request.POST.get
    message = ''
    if request.POST:
        if rg('username') and rg('password') and rg('password2'):
            username = rg('username')
            if User.objects.filter(username=username) or User.objects.filter(username=username):
                message = 'Please enter valid email/username.. already exist'
                varibles = {'message': message}
                return render(request, 'registration/register.html', varibles)
            if not (rg('password') and rg('password2')):
                message = 'Password not matched.'
                varibles = {'message': message}
                return render(request, 'registration/register.html', varibles)
            else:
                client_user = User()
                client_user.username = username
                client_user.set_password(rg('password'))
                client_user.save()
                user = authenticate(username=client_user.username, password=rg('password'))
                if user:
                    login(request, user)
                    subject = 'Account created successfully'
                    return HttpResponseRedirect(reverse('account:dashboard', ))

        else:
            message = 'Please enter valid form'
            varibles = {'message': message}
            return render(request, 'registration/register.html', varibles)
    else:
        return render(request, 'registration/register.html')
