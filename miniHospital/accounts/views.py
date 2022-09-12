from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import Account
from django.contrib import messages, auth


# Create your views here.


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        pswd = request.POST.get('password')
        user = authenticate(request, email=email, password=pswd)
        if user is not None:
            auth.login(request, user)
            # save email in session
            request.session['email'] = email
            if user.is_admin:
                return redirect('admin/')
            if user.is_doctor:
                return redirect('doctorHome')
            elif user.is_lab:
                return redirect('labHome')
            else:
                return redirect('patient-home')
        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('login')
    return render(request, 'accounts/login.html')



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
        user = Account.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username, state=state, district=district, dob=dob, contact=contact, password=password, gender=gender)
        user.is_patient = True
        user.save()
        messages.success(request, 'Thank you for registering with us. Please Login')
        return redirect('login')
    return render(request, 'accounts/signup.html')

def logout(request):
    auth.logout(request)
    return redirect('login')
