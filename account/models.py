from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserOtp(models.Model):
    otp = models.CharField(max_length=5)
    user = models.ForeignKey(User,on_delete=models.CASCADE)