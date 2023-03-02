import datetime
from email import message
from os import lstat
from pydoc import doc
import re
from django.shortcuts import render, render, redirect
# from django.shortcuts import render_to_response
from django.template import RequestContext
from accounts.models import Account
from doctor.models import Specialization
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from .models import patientAppointment
from django.contrib import messages, auth
from doctor.models import Doctor
from leave.models import leaveModel
# from scheduling import SchedulingAlgorithm
from . import scheduling

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.core.mail import send_mail

# Create your views here.


def home(request):
    
    return render(request, 'patient/home.html')


def handler404(request,exception):
    return render(request, 'error/404.html')

def handler500(request):
    return render(request, 'error/500.html')



@login_required(login_url='login')
def patient(request):
    if request.user.is_authenticated:
        if request.user.is_patient:
            email = request.session.get('email')
            usr=Account.objects.get(email=email)
    
            context = {
                'usr':usr,
            }
            return render(request, 'patient/pt-profile.html', context)
        else:
            return redirect('login')
    return redirect('login')

@login_required(login_url='login')
def patientUpdate(request):
    usr=Account.objects.get(email=request.session.get('email'))
    if request.method == 'GET':
        context={}
        context['usr_form']= UserForm(instance=Account.objects.get(email=request.session.get('email')))
        context['usr']=usr
        return render(request, 'patient/pt-update.html', context)
    else:
        form = UserForm(request.POST, request.FILES)
        
        if form.is_valid():
            # email = request.session.get('email')
            usr=Account.objects.get(email=request.session.get('email'))
            usr.first_name = form.cleaned_data['first_name']
            usr.last_name = form.cleaned_data['last_name']
            usr.state = form.cleaned_data['state']
            usr.district = form.cleaned_data['district']
            usr.contact = form.cleaned_data['contact']
            usr.usr_img = form.cleaned_data['usr_img']
            
            usr.dob = form.cleaned_data['dob']
            # print('inside')
            usr.save()
            
            return redirect('patientProfile')
        else:
            context={}
            context['form']= form
            context['usr']=usr
            return render(request, 'patient/pt-update.html', context)



def checkavailability(request):

    d=Doctor.objects.all().values_list('spec_name').distinct()
    doc=Specialization.objects.filter(id__in=d).distinct()
    # get 5 doctors
    doc_list = Doctor.objects.all()[:10]
    print(doc_list)
    # print(spec)
    context={
            'doc': doc,
            'doc_list': doc_list,
    }

    return render(request, 'patient/demo.html', context)

@login_required(login_url='login')
def patientData(request):
    if request.method == 'POST':
        email = request.session.get('email')
        acc=Account.objects.get(email=email)
        usr=patientAppointment()
        is_diabetic = request.POST.get('is_diabetic')
        is_asthma = request.POST.get('is_asthma')
        is_hypertension = request.POST.get('is_hypertension')
        is_stroke = request.POST.get('is_stroke')
        alergetic_drugs = request.POST.get('alergetic_drugs')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        is_alcoholic = request.POST.get('is_alcoholic')
        symptoms = request.POST.get('symptoms')
        
        usr.is_diabetic = is_diabetic
        usr.is_asthma = is_asthma
        usr.is_hypertension = is_hypertension
        usr.is_stroke = is_stroke
        usr.alergetic_drugs = alergetic_drugs
        usr.weight = weight
        usr.height = height
        usr.is_alcoholic = is_alcoholic
        usr.symptoms = symptoms
        usr.email = acc
        usr.save()
        return redirect('checkavailability')

    return render(request, 'patient/patient_data.html')


# @login_required(login_url='login')
def doc_list(request):
    
    lst=Doctor.objects.all()
    for i in lst:
        print(i.email)
    context={
        'doc_list':lst
    }
    return render(request, 'patient/doc_list.html', context)


def singleDoc(request, id):
    lst=Doctor.objects.filter(id=id)
    lst1=Doctor.objects.get(id=id)
    
    yos=datetime.datetime.now().year-lst1.year_of_service
    context={
        'lst':lst,
        'yos':yos
    }
    return render(request, 'patient/single_doc.html', context)



@login_required(login_url='login')
def availability(request):
    if request.method == 'POST':
        email = request.session.get('email')
        date = request.POST.get('date')
        spec = request.POST.get('specialization')
        time=request.POST.get('time')
        request.session['spec'] = spec
        request.session['date'] = date
        request.session['time_div'] = time
        print(request.session['time_div'])
        lv=list(leaveModel.objects.filter(email__is_doctor=True, leaveDate=date, leaveStatus=True, leaveDiv__icontains=time).values_list('email'))
        # print(lv)
        nlst=[i[0] for i in lv]
        # print(nlst)
        lst=list(Doctor.objects.exclude(email__in=nlst).values_list('email'))
        # print(lst)
        slst=[i[0] for i in lst]
        # print(slst)
        spec_lst=Doctor.objects.filter(email__in=lst, spec_name__spec_name=spec)
        
        print(spec_lst)

        
        if spec_lst:
            context={
            'doc':spec_lst
            }
            return render(request, 'patient/availability.html', context)
        else:
            messages.info(request, 'Currently there is no doctor available for this date search another')
            return redirect('checkavailability')
    return render(request, 'patient/availability.html', context)

@login_required(login_url='login')
def appointment(request, id=None):
    doc=Doctor.objects.get(id=id)
    request.session['doc_name']=doc.email.first_name+doc.email.last_name
    request.session['doc_email']=doc.email.email
    request.session['spec']=doc.spec_name.spec_name
    request.session['designation']=doc.des_name.des_name
    return render(request, 'patient/appointment.html')

@login_required(login_url='login')
def confirmappointment(request):
    if request.method == 'POST':
        # email = request.session.get('email')
        # acc=Account.objects.get(email=email)
        usr=patientAppointment()
        is_diabetic = request.POST.get('is_diabetic')
        is_asthma = request.POST.get('is_asthma')
        is_hypertension = request.POST.get('is_hypertension')
        is_stroke = request.POST.get('is_stroke')
        alergetic_drugs = request.POST.get('alergetic_drugs')
        weight = request.POST.get('weight')
        height = request.POST.get('height')
        is_alcoholic = request.POST.get('is_alcoholic')
        symptoms = request.POST.get('symptoms')
        email= request.session['doc_email']
        print(request.session['time_div'])
        # print(email)
        # print('session', request.session['doc_email'])
        # email=Doctor.objects.get(email__email=email)
        # print(email)
        doc_email=email
        # print(doc_email)
        date= request.session['date']
        # time='09:00'
        patient_email=request.user.email
        time_div=request.session['time_div']
        # print(request.session['time_div'])
        # print(time_div)

        timeschedule=scheduling.SchedulingAlgorithm(d_email=doc_email, date=date, time=time_div)
        time=timeschedule.schedule()
        print("exq",time)
        print(time_div)
        if time:
            usr.is_diabetic = is_diabetic
            usr.is_asthma = is_asthma
            usr.is_hypertension = is_hypertension
            usr.is_stroke = is_stroke
            usr.alergetic_drugs = alergetic_drugs
            usr.weight = weight
            usr.height = height
            usr.is_alcoholic = is_alcoholic
            usr.symptoms = symptoms
            usr.doc_email = doc_email
            usr.date = date
            usr.patient_email = patient_email
            usr.time = time
            usr.timeDiv = time_div
            usr.status=True
            usr.save()
            dc=Account.objects.get(email=doc_email)

            current_site = get_current_site(request)
            message = render_to_string('patient/confirmAppointmentEmail.html', {
                'user': usr.id,
                'domain': current_site,
                'doctor_name':dc.first_name+dc.last_name,
                'doctor_spec':request.session['spec'],
                'time':time,
                'date':date,
                'patient_name':request.user.first_name+request.user.last_name,

            })

            send_mail(
                'Confirmation of the Appointment',
                message,
                'minihospitalproject@gmail.com',
                [patient_email],
                fail_silently=False,
            )
            return redirect('viewappointments')
        else:
            messages.info(request, 'Currently there is no doctor available for this date search another')
            return redirect('checkavailability')
            
    return render(request, 'patient/appointment.html')
   



@login_required(login_url='login')
def viewappointments(request):
    lst=patientAppointment.objects.filter(patient_email=request.user.email)
    print(lst)
    context={
        'lst':lst
    }
    return render(request, 'patient/viewappointments.html', context)


def availspec(request,id):
    lst=Doctor.objects.filter(spec_name=id)
    print(lst)
    context={
        'doc_list':lst
    }
    return render(request, 'patient/doc_list.html', context)

def availdoc(request,id):
    lst=Doctor.objects.filter(des_name=id)
    print(lst)
    context={
        'doc_list':lst
    }
    return render(request, 'patient/doc_list.html', context)

def timeslot(request,id):
    # get doctors available time slot based on each day
    lst=Doctor.objects.filter(id=id)
    print(lst)
    context={
        'doc_list':lst
    }
    return render(request, 'patient/doc_list.html', context)