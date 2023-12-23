from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from fashionapp.models import UserProfile, VendorDetails, OrderDetails, ProductDetails, ProductReviews
from django.contrib.auth.models import User

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
            success_message = "Registration successful!"
            return render(req, 'register_user.html',{'success_message': success_message})
        else:
            err_msg = "Passwords do not match"
            return render(req, 'register_user.html', {'er_msg': err_msg})
    return render(req, 'register_user.html')

def vendor(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        email = req.POST.get('email')
        password1 = req.POST.get('password')
        password2 = req.POST.get('confirmPassword')
        mobile = req.POST.get('mobilenumber')
        user_type = 'Vendor'
        if password1 == password2:
            user_profile = UserProfile.objects.create(name=name,email=email,password=password1,mobile_number=mobile,type=user_type)
            return render(req, 'vendor_registration.html', {'user_id': user_profile.id})
        else:
            err_msg = "Passwords do not match"
            return render(req, 'register_vendor.html', {'er_msg': err_msg})
    return render(req, 'register_vendor.html')

def vendor_registration(request):
    er_msg = None
    success_message = None

    if request.method == 'POST':
        business_phone = request.POST.get('business_phone')
        GSTIN_number = request.POST.get('GSTIN_number')
        business_name = request.POST.get('business_name')
        street = request.POST.get('street')
        postal_code = request.POST.get('postal_code')
        city = request.POST.get('city')
        state = request.POST.get('state')

        user_id = UserProfile.objects.latest('id').id

        vendor_details = VendorDetails.objects.create(
            user_profile_id=user_id,
            business_phone=business_phone,
            GSTIN_number=GSTIN_number,
            business_name=business_name,
            street=street,
            postal_code=postal_code,
            city=city,
            state=state
        )

        success_message = "Registration successful!"

    return render(request, 'vendor_registration.html', {'er_msg': er_msg, 'success_message': success_message})
