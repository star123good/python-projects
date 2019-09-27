# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


# Create your views here.
def home(request):
    return render(request, 'home.html')


# Create your views here.
def features(request):
    return render(request, 'features.html')

def pricing(request):
    return render(request, 'pricing.html')

def web_interface(request):
    return render(request, 'web_interface.html')

def plugins(request):
    return render(request, 'plugins.html')

def api_doc(request):
    return render(request, 'api_doc.html')

def contact(request):
    return render(request, 'contact.html')