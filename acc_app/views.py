from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from acc_app.forms import *
from acc_app.models import *
from django.contrib.auth.decorators import login_required
from acc_app.utils import Utils
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.http import HttpResponse
import base64
from django.contrib import messages

@login_required(login_url='/login/')
def index(request):
    return render(request, 'index.html')

def login_user(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(request, email=email, password=password)
    request.session['email'] = email
    if user is not None:
        Utils.send_otp_mobile(user.phone , user)
        return redirect('verify-otp')
    else:
        return render(request, 'login.html')

def verify_otp(request):
    if request.session.has_key('email'):
        email = request.session['email']
        user = User.objects.get(email = email)
        if request.method == 'POST':
            phone_otp = request.POST.get('phone_otp')
            if phone_otp == user.phone_otp:
                user.is_phone_verified = True
                user.phone_otp = None
                user.save()
                login(request, user)
                return redirect('index')

            else:
                context = {'user': user}
                messages.error(request, "Your otp is worng")
                return render(request, 'otp-verification.html', context)

    return render(request, 'otp-verification.html', {'user': user})

def resend_otp(request):
    if request.session.has_key('email'):
        email = request.session['email']
        user = User.objects.get(email = email)
        
        status_new , time = Utils.send_otp_mobile(user.phone, user)

        if not status_new:
            messages.error(request, 'Try after few seconds')
            return redirect('otp-verification')

        else:
            Utils.send_otp_mobile(user.phone, user)
            messages.success(request, 'New otp sent')
            return redirect('otp-verification')
            
    return render(request, 'otp-verification.html')

def logout_user(request):
    logout(request)
    return render(request, 'index.html')

def signup_view(request):
    form = UserAdminCreationForm()
    if request.method == 'POST':
        form = UserAdminCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()
            
            current_site = get_current_site(request).domain
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            relativeLink = reverse('verify-user', kwargs={'uidb64': uidb64, 'token': token})
            absurl = 'http://'+ current_site + relativeLink
            email_body = 'Hi '+ user.email + ', Click below link to verify your account. \n' + absurl
            data = {'email_subject': 'Verify your account', 'email_body': email_body, 'to_email': user.email}
            Utils.send_email(data)  
            return redirect('signup-confirm')

    return render(request, 'signup.html', {'form': form})

def signup_confirm(request):
    return render(request, 'signup-confirm.html')

def verify_user(request, uidb64, token): 
    User = get_user_model()
    try:
        id = smart_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id = id)
    
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    
    if user is not None and PasswordResetTokenGenerator().check_token(user, token):  
        user.is_active = True
        user.is_email_verified = True
        user.save()
        messages.success(request,"You are now verified, please login to continue.")
        return redirect('login')
    else:  
        return HttpResponse('Activation link is invalid!') 
