import email
from operator import ge
from pydoc import doc
from django.shortcuts import render, redirect
from accounts.models import Account
from .models import Doctor
from datetime import date
from .forms import DoctorForm, UserForm
from patient.models import patientAppointment
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
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
    return redirect('login')
            
import cloudinary

@login_required(login_url='login')
def doctorUpdate(request):
    usr=Account.objects.get(email=request.session.get('email'))
    doctor=Doctor.objects.get(email__id=Account.objects.get(email=request.session.get('email')).id)
    if request.method == 'GET':
        context={}
        context['usr_form']= UserForm(instance=Account.objects.get(email=request.session.get('email')))
        context['dr_form']= DoctorForm(instance=Doctor.objects.get(email__id=Account.objects.get(email=request.session.get('email')).id))
        context['usr']=usr
        context['doctor']=doctor
        return render(request, 'doctor/dr-update.html', context)
    else:
        form = UserForm(request.POST, request.FILES)
        doctor = DoctorForm(request.POST)
        # 
        if form.is_valid() and doctor.is_valid():
            # email = request.session.get('email')
            usr=Account.objects.get(email=request.session.get('email'))
            usr.first_name = form.cleaned_data['first_name']
            usr.last_name = form.cleaned_data['last_name']
            usr.state = form.cleaned_data['state']
            usr.district = form.cleaned_data['district']
            usr.contact = form.cleaned_data['contact']
            usr.usr_img = form.cleaned_data['usr_img']
           
            usr.dob = form.cleaned_data['dob']
            print('inside')
            usr.save()
            dr=Doctor.objects.get(email__id=usr.id)
            dr.spec_name = doctor.cleaned_data['spec_name']
            dr.year_of_service = doctor.cleaned_data['year_of_service']
            dr.qual_name = doctor.cleaned_data['qual_name']
            dr.license_no = doctor.cleaned_data['license_no']
            dr.des_name = doctor.cleaned_data['des_name']
            print('inside2')
            dr.save()
            return redirect('doctorHome')

        else:
            context={}
            context['form']= form
            context['doctor']= doctor
            context['usr']=usr
            context['doctor']=doctor
            return render(request, 'doctor/dr-update.html', context)


def doctorAppo(request):
    lst=patientAppointment.objects.filter(doc_email=request.user.email, status=True)
    print(request.user.email)
    print("lst",lst)
    context={
        'lst':lst
    }
    return render(request, 'doctor/viewappo.html', context)