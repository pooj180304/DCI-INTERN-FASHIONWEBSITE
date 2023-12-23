from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('vendor-registration/', views.vendor_registration, name='vendor_registration'),
]

