from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from fashionapp.models import UserProfile, VendorDetails, OrderDetails, ProductDetails, ProductReviews , UserCart
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.urls import reverse
import random
import pandas as pd
import plotly.express as px
from plotly.offline import plot  
import plotly.io as pio
from django.db.models import Avg

def mainpage(req):
    return render(req,'landingpage.html')

def index(request):
    if request.method == 'POST' and 'otp' not in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirmPassword')
        mobile = request.POST.get('mobilenumber')
        user_type = 'Customer'

        if password1 == password2:
            generated_otp = str(random.randint(100000, 999999))
            send_otp_email(email, generated_otp)

            request.session['registration_data'] = {
                'name': name,
                'email': email,
                'password': password1,
                'mobile_number': mobile,
                'user_type': user_type
            }
            request.session['otp'] = generated_otp

            return render(request, 'register_user.html', {'show_otp_input': True})
        else:
            err_msg = "Passwords do not match"
            return render(request, 'register_user.html', {'er_msg': err_msg})

    elif request.method == 'POST' and 'otp' in request.POST:
        entered_otp = request.POST.get('otp')
        saved_otp = request.session.get('otp')

        if entered_otp == saved_otp:
            registration_data = request.session.get('registration_data')
            name = registration_data['name']
            email = registration_data['email']
            password = registration_data['password']
            mobile_number = registration_data['mobile_number']
            user_type = registration_data['user_type']

            UserProfile.objects.create(name=name, email=email, password=password, mobile_number=mobile_number, type=user_type)
            
            del request.session['registration_data']
            del request.session['otp']

            success_message = "Registration successful!"
            return render(request, 'login_user.html')
        else:
            err_msg = "Invalid OTP. Please try again."
            return render(request, 'register_user.html', {'er_msg': err_msg, 'show_otp_input': True})

    return render(request, 'register_user.html')

def send_otp_email(email, otp):
    subject = 'OTP Confirmation'
    message = f'Your OTP is: {otp}'
    from_email = 'minimalsfashion@gmail.com' 

    try:
        send_mail(subject, message, from_email, [email])
        print("Email sent successfully")  
    except Exception as e:
        print(f"Error sending email: {e}")

def vendor(req):
    if req.method == 'POST' and 'otp' not in req.POST:
        name = req.POST.get('name')
        email = req.POST.get('email')
        password1 = req.POST.get('password')
        password2 = req.POST.get('confirmPassword')
        mobile = req.POST.get('mobilenumber')
        user_type = 'Vendor'

        if password1 == password2:
            generated_otp = str(random.randint(100000, 999999))
            send_otp_email(email, generated_otp)

            req.session['registration_data'] = {
                'name': name,
                'email': email,
                'password': password1,
                'mobile_number': mobile,
                'user_type': user_type
            }
            req.session['otp'] = generated_otp

            return render(req, 'register_vendor.html', {'show_otp_input': True})
        else:
            err_msg = "Passwords do not match"
            return render(req, 'register_vendor.html', {'er_msg': err_msg})

    elif req.method == 'POST' and 'otp' in req.POST:
        entered_otp = req.POST.get('otp')
        saved_otp = req.session.get('otp')

        if entered_otp == saved_otp:
            registration_data = req.session.get('registration_data')
            name = registration_data['name']
            email = registration_data['email']
            password = registration_data['password']
            mobile_number = registration_data['mobile_number']
            user_type = registration_data['user_type']

            UserProfile.objects.create(name=name, email=email, password=password, mobile_number=mobile_number, type=user_type)
            
            del req.session['registration_data']
            del req.session['otp']

            success_message = "Registration successful!"
            return render(req, 'vendor_registration.html')
        else:
            err_msg = "Invalid OTP. Please try again."
            return render(req, 'register_vendor.html', {'er_msg': err_msg, 'show_otp_input': True})

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
    if req.method == 'POST':
        mail = req.POST.get('email')
        pw = req.POST.get('password')
        user = get_object_or_404(UserProfile, email=mail)

        if pw == user.password:
            if user.type == 'Customer':
                products = ProductDetails.objects.all().values()
                men_subcategories = ProductDetails.objects.filter(category='Men').values_list('sub_category', flat=True).distinct()
                women_subcategories = ProductDetails.objects.filter(category='Women').values_list('sub_category', flat=True).distinct()
                kids_subcategories = ProductDetails.objects.filter(category='Kids').values_list('sub_category', flat=True).distinct()
                context = {
                    'men_subcategories': men_subcategories,
                    'women_subcategories': women_subcategories,
                    'kids_subcategories': kids_subcategories,
                    'customer': user,
                    'products': products
                }
                
                return render(req, 'customer_homepage.html', context)
            else:
                vend = VendorDetails.objects.filter(user_profile=user)
                return render(req, 'vendor_page.html', {'vendor': user, 'vend': vend[0]})
        else:
            e_msg = 'Incorrect email id or password'
            return render(req, 'login_user.html', {'e_msg': e_msg})

    return render(req, 'login_user.html')

def product_categories_view(request, subcategory,customer_id):
    selected_products = ProductDetails.objects.filter(sub_category=subcategory)  
    context = {
        'selected_subcategory': subcategory,
        'selected_products': selected_products,
        'customer' : customer_id
    }
    return render(request, 'product_categories.html', context)
    
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
        return render(request,"addproduct.html",{ 'id' : vendorid})

def view_orders(request,vendorid):
    orderitems = OrderDetails.objects.filter(vend_id_id=vendorid).values()
    return render(request, 'vieworders.html',{'orders':orderitems})

def order_update(req,ordid):
    orderitems = OrderDetails.objects.filter(product_ordered_id=ordid)

    if req.method == 'POST':
        status = req.POST.get('status')

        # Iterate over the queryset and update each object
        for orderitem in orderitems:
            orderitem.status = status
            orderitem.save()

        return render(req, 'vieworders.html', {'orders': orderitems})

    return render(req, 'status_update.html', {'orders': orderitems})

def display_product(request , vendorid):
    vendorid = vendorid
    products = ProductDetails.objects.filter(product_vendor=vendorid).values()
    return render(request, 'displayproduct.html', {'products':products,'vendor':vendorid})

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

def edit_and_save_customer_profile(request, customerid):
    user_details = get_object_or_404(UserProfile, id=customerid)

    if request.method == 'POST':
        user_details.name = request.POST.get('name')
        user_details.email = request.POST.get('email')
        user_details.mobile_number = request.POST.get('mobile_number')
        user_details.save()

        return redirect('customer_profile', customer_id=customerid)

    return render(request, 'edit_customer_profile.html', {'user_details': user_details})

def add_to_cart(request , customer_id , product_id):
    cart_details = UserCart(
        cart_userid = customer_id,
        cart_product = product_id
    )

    product = get_object_or_404(ProductDetails, product_id=product_id)
    existing_cart_item = UserCart.objects.filter(cart_userid=customer_id, cart_product=product_id).first()

    if existing_cart_item:
        existing_cart_item.quantity += 1
        existing_cart_item.cost = product.cost * existing_cart_item.quantity
        existing_cart_item.save()
    else:
        cart_details = UserCart(
            cart_userid=customer_id,
            cart_product=product_id,
            quantity=1,
            cost = product.cost
        )
        cart_details.save()

    return HttpResponse("stored")

def cart(request, customer_id):
    cart = UserCart.objects.filter(cart_userid=customer_id).values()
    cart_products = ProductDetails.objects.filter(product_id__in=cart.values_list('cart_product', flat=True))
    user = UserProfile.objects.get(id=customer_id)
    cus = customer_id
    cart_and_cost = zip(cart_products, cart)
    quantity_range = range(1,7)
    total_cost = sum(item['cost'] for item in cart)

    return render(request, 'cart.html', {'cart_and_cost': cart_and_cost, 'cus': cus,'quantity_range': quantity_range,'total_cost': total_cost})

def update_quantity(request, cust_id):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 0))
    user_cart = get_object_or_404(UserCart, cart_product=product_id, cart_userid=cust_id)
    product_details = get_object_or_404(ProductDetails, product_id=product_id)

    user_cart.quantity = quantity
    user_cart.cost = quantity * product_details.cost  
    user_cart.save()

    return redirect('cart', customer_id=cust_id)
    return render(request , 'cart.html' , {'cart':cart_products , 'user':user})

def delete_product(request, customer_id, product_id):
    product = UserCart.objects.filter(cart_product=product_id)
    product.delete()
    cart_url = reverse('cart', kwargs={'customer_id': customer_id})
    return redirect(cart_url)
    
def edit_product(request, product_id):
    product_details = get_object_or_404(ProductDetails, product_id=product_id)

    if request.method == 'POST':
        product_details.product_vendor = request.POST.get('product_vendor')
        product_details.product_name = request.POST.get('product_name')
        product_details.availability = request.POST.get('availability')
        product_details.size = request.POST.get('size')
        product_details.colours = request.POST.get('colours')
        product_details.description = request.POST.get('description')
        product_details.cost = request.POST.get('cost')
        product_details.category = request.POST.get('category')
        product_details.sub_category = request.POST.get('sub_category')

        new_images = request.FILES.get('images')
        if new_images:
            product_details.images = new_images

        product_details.save()

        return redirect('display_product', vendorid=product_details.product_vendor)

    return render(request, 'editproduct.html', {'product_details': product_details})

def place_orderdetails(request,customer_id , product_id ):
    product_details = get_object_or_404(ProductDetails, product_id=product_id)
    customer = get_object_or_404(UserProfile, id=customer_id)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        payment_type = request.POST.get('payment_type')
        address = request.POST.get('address')
        create_order(product_details, customer, quantity, payment_type, address)

        return HttpResponse("Ordered placed") 
    return render(request,"place_orderdetails.html",{'place_order':product_details,'customer_detail':customer})


def create_order(product, customer, quantity, payment_type, address):
    vendor = VendorDetails.objects.get(user_profile__id=product.product_vendor)

    try:
        quantity = int(quantity)

        if product.availability >= quantity > 0:
            order = OrderDetails(
                product_ordered=product,
                cust_id=customer,
                vend_id=vendor,
                quantity=quantity,
                payment_details=payment_type,
                address=address,
                status='Ordered',
                cost=product.cost * quantity  
            )
            order.save()

            product.availability -= quantity
            product.save()

            return True 
        else:
            return False  
    except ValueError:
       
        return False

def confirm_order(request,customer_id):
    orders = OrderDetails.objects.filter(cust_id_id = customer_id)
    product_details_list = []

    # Loop through each order and get the associated product details
    for order in orders:
        product = ProductDetails.objects.get(product_id=order.product_ordered_id)
        product_details_list.append({
            'order': order,
            'product': product,
        })

    # Retrieve the order details for the given product
    # confirm = OrderDetails.objects.filter(product_ordered_id=product.product_id)

    return render(request, "confirm_order.html", {"product": product_details_list})
    

def delete_product(request, customer_id, product_id):
    product = UserCart.objects.filter(cart_product=product_id)
    product.delete()
    cart_url = reverse('cart', kwargs={'customer_id': customer_id})
    return redirect(cart_url)
    
def customer_profile(request, customer_id):
    try:
        user_details = UserProfile.objects.get(id=customer_id)
    except UserProfile.DoesNotExist:
        return render(request, 'customer_homepage.html')  
    return render(request, 'customerprofile.html', {'customer_details': user_details})

def landing_page_view(request):
    return render(request, 'landingpage.html')

def product_details(request, product_id, cust_id):
    product = get_object_or_404(ProductDetails, product_id=product_id)
    customer = get_object_or_404(UserProfile, id=cust_id)
    reviews = ProductReviews.objects.filter(review_pid_id=product_id)
    overall_rating = ProductReviews.objects.filter(review_pid=product).aggregate(Avg('ratings'))['ratings__avg']

   
    star_ratings = {}
    for i in range(1, 6):
        count = reviews.filter(ratings=i).count()
        total_reviews = reviews.count()
        percentage = (count / total_reviews) * 100 if total_reviews > 0 else 0
        star_ratings[i] = round(percentage, 2)

    context = {
        'product': product,
        'customer': customer,
        'reviews': reviews,
        'overall_rating': overall_rating,
        'star_ratings': star_ratings,
    }
    return render(request, 'product_display.html', context)

from django.shortcuts import render

def visualize(request, vendor_id):
    # Load the dataset
    df = pd.read_csv("./fashionapp/product_dataset_with_order_details.csv")

    # Function to filter data for a specific vendor
    def filter_data_by_vendor(vendor_id):
        return df[df['product_vendor'] == vendor_id]

    # Convert vendor_id to integer (if needed)
    vendor_id = int(vendor_id)

    # Filter data for the input vendor
    vendor_data = filter_data_by_vendor(vendor_id)

    # Create Plotly figures
    fig1 = px.bar(vendor_data, x='product_name', y='cost', title=f'Sales Performance for Vendor {vendor_id}', labels={'cost': 'Sales (in $)'}, text='cost', height=400)
    fig1.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig1.update_layout(xaxis_tickangle=-45, xaxis_title='Product Name', yaxis_title='Sales (in $)')
    plot_div1 = plot(fig1, output_type='div', include_plotlyjs=False)

    fig2 = px.line(vendor_data.groupby('month')['cost'].sum().reset_index(), x='month', y='cost', title=f'Monthly Sales Trend for Vendor {vendor_id}', labels={'cost': 'Total Sales (in $)'}, markers=True, line_shape='linear')
    fig2_div = plot(fig2, output_type='div', include_plotlyjs=False)

    fig3 = px.pie(vendor_data['order_status'].value_counts(), names=vendor_data['order_status'].value_counts().index, title=f'Order Status Distribution for Vendor {vendor_id}', labels={'label': 'Order Status'}, hole=0.3)
    fig3_div = plot(fig3, output_type='div', include_plotlyjs=False)

    fig4 = px.bar(vendor_data, x='category', y='cost', title=f'Category-wise Sales for Vendor {vendor_id}', labels={'cost': 'Sales (in $)', 'category': 'Category'}, text='cost', height=400)
    fig4.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig4_div = plot(fig4, output_type='div', include_plotlyjs=False)

    fig5_modified = px.bar(vendor_data.groupby(['month', 'delivery_address'])['cost'].sum().reset_index(), x='month', y='cost', color='delivery_address', title=f'Monthly State-wise Revenue for Vendor {vendor_id}', text='cost', height=400)
    fig5_modified.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig5_modified_div = plot(fig5_modified, output_type='div', include_plotlyjs=False)

    # Pass the HTML strings to the template along with vendor_id
    return render(request, 'visualize.html', {'vendor_id': vendor_id, 'plot_div1': plot_div1, 'fig2_div': fig2_div, 'fig3_div': fig3_div, 'fig4_div': fig4_div, 'fig5_modified_div': fig5_modified_div})

def prod_rev(req, cust_id,prodid):
    if req.method == 'POST':
        rev = req.POST.get('review')
        rate = int(req.POST.get('rating'))
        product = ProductDetails.objects.get(product_id=prodid)
        ProductReviews.objects.create(product_review=rev, ratings=rate, review_pid=product)
        return redirect('product_details', cust_id=cust_id, product_id=prodid)
    return render(req, 'add_comments.html',{'product':prodid,'customer':cust_id})