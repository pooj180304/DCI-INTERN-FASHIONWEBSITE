from django.http import HttpResponse
from django.shortcuts import render
from fashionapp.models import UserProfile, VendorDetails, OrderDetails, ProductDetails, ProductReviews

def index(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        password1 = req.POST.get('password')
        password2 = req.POST.get('confirmPassword')
        mobile = req.POST.get('mobilenumber')
        user_type = 'Customer'
        if password1 == password2:
            UserProfile.objects.create(name=name,email=email,password=password1,mobile_number=mobile,type=user_type)
            return render(req, 'index.html')
        else:
            err_msg = "Passwords do not match"
            return render(req, 'index.html', {'er_msg': err_msg})
    return render(req, 'index.html')
