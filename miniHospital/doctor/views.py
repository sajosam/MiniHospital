import email
from pydoc import doc
from django.shortcuts import render, redirect
from accounts.models import Account
from .models import Doctor
from datetime import date

# Create your views here.


def doctorHome(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:
            email = request.session.get('email')
            print(email)
            # access details of doctor in account table
            usr=Account.objects.get(email=email)
            # access profile details in doctor tablet
            doctor=Doctor.objects.get(email__id=usr.id)
            # ex=list(Doctor.objects.filter(email__id=usr.id).values_list('year_of_service',flat=True))
            print(usr.id)
            print(doctor)
            # print(ex)
    
            
            context = {
                'doctor': doctor,
                'usr':usr,
                'exp':date.today().year-doctor.year_of_service,
            }
            return render(request, 'doctor/dr-profile.html', context)
        else:
            return redirect('login')
            