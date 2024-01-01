from django.db import models

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    mobile_number = models.CharField(max_length=15)
    type = models.CharField(max_length=50)

class VendorDetails(models.Model):
    user_profile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, unique=True)
    business_phone = models.CharField(max_length=15)
    GSTIN_number = models.CharField(max_length=15)
    business_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

class ProductDetails(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_vendor = models.IntegerField()  
    product_name = models.CharField(max_length=255)
    availability = models.IntegerField()
    size = models.CharField(max_length=15)
    colours = models.CharField(max_length=55)
    description = models.CharField(max_length=555)
    cost = models.IntegerField()
    images = models.ImageField(upload_to="images/")
    category = models.CharField(max_length=35)
    sub_category = models.CharField(max_length=35)

class OrderDetails(models.Model):
    product_ordered = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    cust_id = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vend_id = models.ForeignKey(VendorDetails, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    payment_details = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    status = models.CharField(max_length=60)
    cost = models.IntegerField()
    invoice_number = models.AutoField(primary_key=True)

class ProductReviews(models.Model):
    product_review = models.CharField(max_length=255)
    review_pid = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    ratings = models.IntegerField()
    @property
    def star_range(self):
        return range(self.ratings)

    @property
    def empty_star_range(self):
        return range(5 - self.ratings)

class UserCart(models.Model):
    cart_userid = models.IntegerField()
    cart_product=models.IntegerField()
    quantity = models.IntegerField(default=1)
    


