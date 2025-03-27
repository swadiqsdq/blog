from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from .models import *

import random

# Create your views here.

def user_register(request):
    if request.method == 'POST':
        strUserName = request.POST.get('username')
        strFirstName = request.POST.get('firstname')
        strLastName = request.POST.get('lastname')
        strEmail = request.POST.get('email')
        strPassword1 = request.POST.get('password1')
        strPassword2 = request.POST.get('password2')

        if strUserName and strPassword1 and strPassword2:
        
            if strPassword1 == strPassword2:
                user = User.objects.filter(username=strUserName)
                if not user:
                    User.objects.create_user(
                        username=strUserName,
                        first_name=strFirstName,
                        last_name=strLastName,
                        email=strEmail,
                        password=strPassword2
                    )
                    messages.success(request,'Registration successful')
                    return redirect('login')
                else:
                    messages.error(request,request, 'User name already exist')  
            else:
                messages.error(request,'password not matches')
        else:
            messages.error(request,'fill form properly')

    return render(request,'account/register.html')


def userLogin(request):
    if request.method == "POST":
        strUserName = request.POST.get('username')
        strPassword = request.POST.get('password')

        user = authenticate(username=strUserName,password=strPassword)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'invalid username or password')
    return render(request,'account/login.html')

def userLogout(request):
    logout(request)
    return redirect('login')

def changePassword(request,username):
    user = User.objects.get(username=username)    
    if username:
        user = User.objects.get(username=username)
        if request.method == "POST":
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            if password1 ==  password2:
                user.set_password(password2)
                user.save()
                messages.success(request,'password is updated')
                return redirect('login')
            messages.error (request,'password doesn\'t match')              
    return render(request,'account/changePassword.html')


def forgotPassword(request):

    if request.method == "POST":

        username = request.POST.get('username')

        user = User.objects.filter(username=username)

        if user:
            email = user.first().email
            otp = random.randrange(100000,999999)
            from_email = 'muhammedswadiqsdq@gmail.com'
            to = [email]
            subject = 'Your OTP for Secure Access to Blog'
            message = f"""Hi {username},

Your One-Time Password (OTP) is: {otp}
This OTP is valid for 10 minutes. Please do not share it with anyone.
If you didn't request this OTP, contact our support team at muhammedswadiqsdq@gmail.com.

Best regards,  
Team Blog"""
      
            send_mail(
                subject = subject,
                message = message,
                from_email = from_email,
                recipient_list = to,
                fail_silently=False
            )

            UserOtp.objects.update_or_create(
                user = user.first(),

                defaults={
                    'otp':otp
                }
            )
            messages.success(request,'OTP sent succussfully!')
            return redirect ('otp_verify',username)
        
        messages.error(request,'username doesn\'t exist !!! ')


    return render(request,'account/forgotPassword.html')

def otp_verify(request,username):
    user = User.objects.get(username=username)

    if request.method == "POST":
        otp_obj = UserOtp.objects.get(user=user)
        # Retrieve the list of OTP digits from the form
        otp_digits = request.POST.getlist('otp')
        
        # Combine the digits into a single string
        entered_otp = ''.join(otp_digits)

        if otp_obj.otp == entered_otp:
            messages.success(request,'OTP is verified')
            return redirect('changePassword',username)

    return render(request,'account/verifyOtp.html',{'email':user.email})