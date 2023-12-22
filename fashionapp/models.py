from django.db import models

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  
    mobile_number = models.CharField(max_length=15)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.id

class VendorDetails(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    business_phone = models.CharField(max_length=15)
    GSTIN_number = models.CharField(max_length=15)
    business_name = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.business_name} ({self.user_profile.name})"