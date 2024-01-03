from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainpage, name='mainpage'),
    path('register_user',views.index,name='register_user'),
    path('otp_confirmation/', views.index, name='otp_confirmation'),
    path('otp_confirm/', views.vendor, name='otp_confirm'),
    path('vendor-registration/', views.vendor_registration, name='vendor_registration'),
    path('vendor/', views.vendor, name='vendor'),
    path('login/', views.user_login, name='login'),
    path('add_product/<int:vendorid>/', views.add_product, name='add_product'),
    path('view_orders/<int:vendorid>/', views.view_orders, name='view_orders'),
    path('display_product/<int:vendorid>/', views.display_product, name='display_product'),
    path('visualize/<int:vendor_id>/', views.visualize, name='visualize'),
    path('vendor_profile/<int:vendorid>/', views.vendor_profile, name='vendor_profile'),
    path('edit_and_save_vendor_profile/<int:vendorid>/', views.edit_and_save_vendor_profile, name='edit_and_save_vendor_profile'),
    path('store_product/<int:vendorid>/', views.store_product, name='store_product'),
    path('add_to_cart/<int:customer_id>/<int:product_id>/', views.add_to_cart, name='add_tocart'),
    path('cart/<int:customer_id>/',views.cart, name='cart'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('place_orderdetails/<int:customer_id>/<int:product_id>/',views.place_orderdetails,name="place_orderdetails"),
    path('delete_product/<int:customer_id>/<int:product_id>/', views.delete_product, name='delete_product'),
    path('landingpage/', views.landing_page_view, name='landing_page_view'),
    path('customer_profile/<int:customer_id>/', views.customer_profile, name='customer_profile'),
    path('products/<str:subcategory>/<int:customer_id>/', views.product_categories_view, name='product_categories'),
    path('products/<str:subcategory>/', views.product_categories_view, name='product_categories'),
    path('confirm_order/<int:customer_id>/', views.confirm_order , name="confirm_order"),
    path('order_update/<int:ordid>/', views.order_update, name='order_update'),
    path('product_details/<int:cust_id>/<int:product_id>/', views.product_details, name='product_details'),
    path('order_update/<int:ordid>/', views.order_update, name='order_update'),
    path('prod_rev/<int:cust_id>/<int:prodid>/',views.prod_rev,name="prod_rev"),
]

