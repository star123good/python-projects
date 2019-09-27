from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'charge/', views.charge,name='charge'),
    url(r'makepayment', views.PaymentPageView.as_view(),name="payment"),
    url(r'subscription/', views.SubscriptionView,name="subscription"),

]
