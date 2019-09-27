"""
Module containg the url configs for the dashboard module
"""

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^dashboard$', views.dashboard, name='dashboard'),
    url(r'^api_dashboard/$', views.api_dashboard, name='api_dashboard'),
    url(r'^api_dashboard/(?P<command_type>\w+)/$', views.api_dashboard, name='api_dashboard'),
    url(r'^account_overview$', views.account_overview, name='account_overview'),
    url(r'^web_interface_pro$', views.web_interface_pro, name='web_interface_pro'),
    url(r'^delivered_webhooks$', views.delivered_webhooks, name='delivered_webhooks'),
    url(r'^plans_and_billing$', views.plans_and_billing, name='plans_and_billing'),
    # url(r'^adding_billing_info$', views.adding_billing_info, name='adding_billing_info'),
    url(r'^redeem_coupon$', views.redeem_coupon, name='redeem_coupon'),
    url(r'^plans_info$', views.plans_info, name='plans_info'),
    #url(r'^adding_billing_info$', views.adding_billing_info, name='adding_billing_info'),
    url(r'^file_uploader$', views.file_uploader, name='file_uploader'),
    url(r'^url_paster$', views.url_paster, name='url_paster'),
    url(r'^billing/payment/(?P<payment_type>\w+)/$', views.adding_billing_info, name='adding_billing_info'),
    url(r'^page_cruncher$', views.page_cruncher, name='page_cruncher'),
    url(r'^web_interface_pro_upload_files/ajax$', views.web_interface_pro_upload_files, name='web_interface_pro_upload_files'),
    url(r'^page_cruncher_uploader/ajax$', views.page_cruncher_uploader_ajax, name='page_cruncher_uploader_ajax'),
    url(r'^url_paster_uploader/ajax$', views.url_paster_uploader_ajax, name='url_paster_uploader_ajax'),
]
