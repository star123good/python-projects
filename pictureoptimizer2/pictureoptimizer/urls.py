"""pictureoptimizer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.contrib.auth import views as auth_views
from account.views import registration
from account.views_auth import *
from rest_framework import routers
from . import stripeviews as stripe_view

# Routers provide a way of automatically determining the URL conf.
router = routers.DefaultRouter()
#router.register(r'account', stripe_view.AccountViewSet)
router.register(r'charge', stripe_view.ChargeViewSet)
router.register(r'customer', stripe_view.CustomerViewSet)
router.register(r'plan', stripe_view.PlanViewSet)
router.register(r'subscription', stripe_view.SubscriptionViewSet)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^payments/', include('payments.urls')),
    url(r'^', include('website.urls', namespace='website')),
    url(r'^account/login', auth_views.login, name='login'),
    url(r'^accounts/login', auth_views.login, name='login'),
    url(r'^account/logout', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'^account/registration$', registration, name='registration'),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^account/reset_password$', ResetPasswordRequestView.as_view(), name="reset_password"),
    url(r'^account/reset_password_confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
]
urlpatterns += router.urls