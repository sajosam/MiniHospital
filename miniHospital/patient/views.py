from email import message
import re
from django.shortcuts import render, render, redirect
# from django.shortcuts import render_to_response
from django.template import RequestContext
from accounts.models import Account
from .forms import UserForm
from django.contrib.auth.decorators import login_required
from .models import PatientData, appointment
from django.contrib import messages, auth


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
            # usr.email = form.cleaned_data['email']
            # usr.password = form.cleaned_data['password']
            # usr.username = form.cleaned_data['username']
            usr.dob = form.cleaned_data['dob']
            # print('inside')
            usr.save()
            
            return redirect('patientProfile')
        else:
            context={}
            context['form']= form
            context['usr']=usr
            return render(request, 'patient/pt-update.html', context)



def Appointment(request):
    if request.method == 'POST':
        email = request.session.get('email')
        acc=Account.objects.get(email=email)
        usr=appointment()
        symptoms = request.POST.get('symptoms')
        date = request.POST.get('date')
        time = request.POST.get('time')
        usr.date = date
        usr.time = time
        usr.symptoms = symptoms
        usr.p_email = acc.email
        usr.email = acc
        usr.save()
        # message
        messages.success(request, 'Appointment Booked Successfully, check your email for more details')
        return redirect('patientProfile')
    return render(request, 'patient/appointment.html')

def patientData(request):
    if request.method == 'POST':
        email = request.session.get('email')
        acc=Account.objects.get(email=email)
        usr=PatientData()
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
        return redirect('appointment')

    return render(request, 'patient/patient_data.html')


def doc_list(request):
    return render(request, 'patient/doc_list.html')