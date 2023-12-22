from django.db import models

# Create your models here.
class user_Details(models.Model):
    name = models.CharField(max_length=256)
    