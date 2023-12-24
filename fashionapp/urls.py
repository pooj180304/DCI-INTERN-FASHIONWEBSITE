from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vendor-registration/', views.vendor_registration, name='vendor_registration'),
    path('vendor/', views.vendor, name='vendor'),
    path('login/', views.user_login, name='login'),
    path('add_product/<int:vendorid>/', views.add_product, name='add_product'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('display_product/<int:vendorid>/', views.display_product, name='display_product'),
    path('visualize/', views.visualize, name='visualize'),
    path('vendor_profile/<int:vendorid>/', views.vendor_profile, name='vendor_profile'),
    path('store_product/<int:vendorid>/', views.store_product, name='store_product'),
]
