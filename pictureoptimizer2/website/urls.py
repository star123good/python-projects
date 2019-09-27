"""
Module containg the url configs for the dashboard module
"""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^features$', views.features, name='features'),
    url(r'^pricing$', views.pricing, name='pricing'),
    url(r'^web_interface$', views.web_interface, name='web_interface'),
    url(r'^plugins$', views.plugins, name='plugins'),
    url(r'^api_doc$', views.api_doc, name='api_doc'),
    url(r'^contact$', views.contact, name='contact'),
]