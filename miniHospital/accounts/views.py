import random
from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.http import HttpResponse
from .helper import *

# from miniHospital.miniHospital.settings import EMAIL_HOST_USER
from .models import Account,Otp
from django.contrib import messages, auth
from .forms import ContactForm

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail




def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pswd = request.POST.get('password')
        request.session['email'] = email
        request.session['password'] = pswd
        print(request.session['email'],request.session['password'])
        user = authenticate(request, email=email, password=pswd)
        # user=Account.objects.filter(email=email,password=pswd)
        if user and user.is_active:
            id=user.id
            phone=user.contact
            email=user.email
            id=Account.objects.only('id').get(email=email)
        
        if user:
            # auth.logout(request)
            otp=random.randint(100000,999999)
            profile=Otp.objects.create(user_id=id,otp=otp,phone=phone)
            messagehadler=MessageHandler(phone,otp).send_otp_via_message()
            print(messagehadler)
            print(profile)
            print(profile.uid)
            print(profile.id)
            red=redirect('otp',uid=profile.uid)
            red.set_cookie("can_otp_enter",True,max_age=600)
            return red
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
        
    form=ContactForm()
    return render(request, 'accounts/login.html',{'form':form})



def signup(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        username = email.split('@')[0]
        state = request.POST.get('state')
        district = request.POST.get('district')
        dob= request.POST.get('dob')
        contact = request.POST.get('contact')
        password = request.POST.get('password')
        gender = request.POST.get('gender')
        # check if user already exists
        if Account.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('signup')
        user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, state=state, district=district, dob=dob, contact=contact, password=password, gender=gender)
        user.is_patient = True
        # user.save()
        messages.success(request, 'Thank you for registering with us. Please Login')


        current_site = get_current_site(request)
        message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

        send_mail(
                'Please activate your account',
                message,
                'maindemo578@gmail.com',
                [email],
                fail_silently=False,
            )
        

        return redirect('/accounts/login/?command=verification&email='+email)
        # return redirect('login')
    return render(request, 'accounts/signup.html')

def logout(request):
    auth.logout(request)
    return redirect('login')


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Congratulations! Your account is activated.')
        return redirect('patData')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('register')

from django.core.mail import EmailMessage


def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if Account.objects.filter(email=email).exists():
            user = Account.objects.get(email__exact=email)

            current_site = get_current_site(request)
            message = render_to_string('accounts/reset_password_email.html', {
                'user': user,
                'domain': current_site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(
                'Please activate your account',
                message,
                'maindemo578@gmail.com',
                [email],
                fail_silently=False,
            )
            
            messages.success(request, 'Password reset email has been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Account does not exist!')
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')

def resetpassword_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has been expired!')
        return redirect('login')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('resetPassword')
    else:
        return render(request, 'accounts/resetPassword.html')


def change_password(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = Account.objects.get(email__exact=request.user.email)
        success = user.check_password(current_password)
        if success:
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password updated successfully.')
            return redirect('login')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_password')
    return render(request, 'accounts/change_password.html')

def otpVerify(request,uid):
    if request.method=="POST":
        profile=Otp.objects.get(uid=uid)   
        o=int(request.POST['otp'])
        if request.COOKIES.get('can_otp_enter')!=None:
            if(profile.otp==o):
                email=request.session['email']
                password=request.session['password']

                user = auth.authenticate(email=email, password=password)
                auth.login(request, user)
#             # save email in session
                if user.is_admin:
                    return redirect('http://127.0.0.1:8000/admin/dashboard/')
                if user.is_doctor:
                    return redirect('doctorHome')
                elif user.is_lab:
                    return redirect('labhome')
                else:
                    return redirect('patientHome')
                

            messages.error(request,"Invalid OTP")
            return redirect("otp",uid=uid)
        messages.error(request,"Please enter OTP")
        return redirect("otp",uid=uid)

    return render(request,"accounts/otp.html",{'id':uid})

def privacy(request):
    return render(request,"accounts/privacy.html")