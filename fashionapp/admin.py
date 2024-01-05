from django.contrib import admin
from .models import UserProfile, VendorDetails, OrderDetails, ProductDetails, ProductReviews , UserCart
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(VendorDetails)
admin.site.register(OrderDetails)
admin.site.register(ProductDetails)
admin.site.register(ProductReviews)
admin.site.register(UserCart)