from django.db import models

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  
    mobile_number = models.CharField(max_length=15)
    type = models.CharField(max_length=50)

    def __str__(self):
        return self.name
