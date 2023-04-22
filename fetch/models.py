from django.db import models
from django.utils import timezone
from datetime import timedelta
import random

# models.py

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Position(models.Model):
    title =models.CharField(max_length =50)
   
    def __str__(self):
        return f"{self.title} {self.title}"

class EmployeeRefer(models.Model):
    firstname= models.CharField(max_length=255,default="FirstName")
    lastname = models.CharField(max_length=255,default="LastName")
    emailid  =models.EmailField(max_length=100,default="emailid")
    phonenumber = models.CharField(max_length =10,default ="0")
    Experience =models.IntegerField(default =0)
    Description = models.CharField(max_length =700,default="Skills Set")
    position =models.ForeignKey(Position,on_delete =models.CASCADE)
    Relation = models.CharField(default="Friend")
    UploadResume = models.FileField(default=None)

    
    def __str__(self):
        return f"{self.firstname} {self.lastname}"
from django.contrib.auth.models import User

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    expires_at = models.DateTimeField(default=timezone.now)
    def generate_otp(user):
        # Generate OTP for the user
        try:
            otp_instance = OTP.objects.get(user=user)
            otp_instance.delete()  # Delete existing OTP instance
        except OTP.DoesNotExist:
            pass
        otp = str(random.randint(1000, 9999))
        print(otp)
        expires_at = timezone.now() + timedelta(minutes=1)  # Set OTP expiration time to 5 minutes from now
        otp_instance = OTP(user=user, otp=otp, expires_at=expires_at)
        otp_instance.save()
        return otp

    def is_valid(self):
        # Check if OTP is valid based on expiration time
        return timezone.now() <= self.expires_at


    def __str__(self):
        return f'OTP for {self.user.username}'
    
class PDFFile(models.Model):
   
    pdf_file = models.FileField(upload_to='pdfs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

