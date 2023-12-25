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
            return render(req, 'login_user.html')
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

    return render(request, 'login_user.html')

def user_login(req):
    if req.method=='POST':
        mail = req.POST.get('email')
        pw = req.POST.get('password')
        type = req.POST.get('userType')
        user = get_object_or_404(UserProfile, email=mail)
        if pw==user.password:
            if user.type=='Customer':
                products = products = ProductDetails.objects.all().values()
                return render(req,'customer_page.html',{'customer':user,'products':products})
            else:
                return render(req,'vendor_page.html' , {'vendor':user})
        else:
            e_msg = 'incorrect email id or password'
            return render(req,'login_user.html',{'e_msg':e_msg})
    return render(req,'login_user.html')

def add_product(request , vendorid):
    return render(request, 'addproduct.html' , { 'id' : vendorid})


def store_product(request, vendorid):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        availability = request.POST.get('availability')
        size = request.POST.get('size')
        colours = request.POST.get('colours')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        images = request.FILES.get('images')
        category = request.POST.get('category')
        sub_category = request.POST.get('sub_category')   

        product_details = ProductDetails(
            product_vendor=vendorid,
            product_name=product_name,
            availability=availability,
            size=size,
            colours=colours,
            description=description,
            cost=cost,
            images = images,
            category=category,
            sub_category=sub_category
        )

        product_details.save()
        return HttpResponse("stored")

def view_orders(request):
    return render(request, 'vieworders.html')

def display_product(request , vendorid):
    products = ProductDetails.objects.filter(product_vendor=vendorid).values()
    return render(request, 'displayproduct.html', {'products':products})

def visualize(request):
    return render(request, 'visualize.html')

def vendor_profile(request, vendorid):
    try:
        vendor_details = VendorDetails.objects.get(user_profile_id=vendorid)
    except VendorDetails.DoesNotExist:
        return render(request, 'vendor_page.html')  
    return render(request, 'vendorprofile.html', {'vendor_details': vendor_details})

def edit_and_save_vendor_profile(request, vendorid):
    vendor_details = get_object_or_404(VendorDetails, user_profile_id=vendorid)

    if request.method == 'POST':
        vendor_details.user_profile.name = request.POST.get('name')
        vendor_details.user_profile.email = request.POST.get('email')
        vendor_details.user_profile.mobile_number = request.POST.get('mobile_number')
        vendor_details.business_name = request.POST.get('business_name')
        vendor_details.business_phone = request.POST.get('business_phone')
        vendor_details.GSTIN_number = request.POST.get('GSTIN_number')
        vendor_details.street = request.POST.get('street')
        vendor_details.postal_code = request.POST.get('postal_code')
        vendor_details.city = request.POST.get('city')
        vendor_details.state = request.POST.get('state')

        vendor_details.user_profile.save()
        vendor_details.save()

        return redirect('vendor_profile', vendorid=vendorid)

    return render(request, 'edit_vendor_profile.html', {'vendor_details': vendor_details})
