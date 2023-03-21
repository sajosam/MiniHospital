import email
from operator import ge
from pydoc import doc
import random
from django.shortcuts import render, redirect,HttpResponse
from accounts.models import Account
from .models import Doctor,Prescription
from datetime import date
from .forms import DoctorForm, UserForm, appointmentForm, prescriptionForm, prescriptionFormReadyonly
# from patient.models import patientAppointment
from django.contrib.auth.decorators import login_required
from patient.models import appointmentconfirmation
from lab.models import labReport


# Create your views here.

@login_required(login_url='login')
def doctorHome(request):
    if request.user.is_authenticated:
        if request.user.is_doctor:
            email = request.session['email']
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
    data=appointmentconfirmation.objects.filter(doc_email=request.user.id,appo_status__in=('accepted','completed'))
    context={
        'data':data,
    }
    return render(request, 'doctor/viewappo.html',context)

def viewpatient(request,id=None):
    print("1")
    request.session['appo_id']=id
    if Prescription.objects.filter(appoint_id=id).exists():
        print("2")
        data=prescriptionFormReadyonly(instance=Prescription.objects.get(appoint_id=id))
        appo=appointmentconfirmation.objects.get(id=id)
        context={}
        context['data']=data
        context['appo']=appo
        context['id']=id
        if Prescription.objects.get(appoint_id=id).lab_report!=None:
            lab=Prescription.objects.get(appoint_id=id).lab_report
            if lab!=None:
                context['lab']=lab
        print(context['lab'])
        return render(request, 'doctor/moredetails.html',context)
    else:
        print("3")
        if request.method == 'POST':
            print("4")
            data=prescriptionForm(request.POST)
            print(data.errors)
            if data.is_valid():
                prescription=data.cleaned_data['prescription']
                data.symptoms=data.cleaned_data['symptoms']
                diagnosis=data.cleaned_data['diagnosis']
                lab_report=data.cleaned_data['lab_report']

                def getuniqueid():
                    lab_uidd=random.randint(100000,999999)
                    if lab_uidd in Prescription.objects.values_list('lab_uidd',flat=True):
                        lab_uidd=getuniqueid()
                    return lab_uidd
                appoint_id=appointmentconfirmation.objects.get(id=request.session.get('appo_id'))
                print("appo",appoint_id)
                print("appo1",appoint_id.user_id.id)

                if lab_report!=None:
                    lab_uidd=getuniqueid()
                    da=labReport.objects.create(lab_uidd=lab_uidd,appoint_id=appoint_id,patient_id=appoint_id.user_id.id)
                else:
                    lab_uidd=None
                appoint_id=appointmentconfirmation.objects.get(id=request.session.get('appo_id'))
                d=Prescription.objects.create(prescription=prescription,symptoms=data.symptoms,diagnosis=diagnosis,lab_report=lab_report,appoint_id=appoint_id,lab_uidd=lab_uidd)
                if da:
                    da.prescription_id=Prescription.objects.only('id').get(appoint_id=appoint_id)
                d.save()
                da.save()
                appo=appointmentconfirmation.objects.get(id=id)
                appo.appo_status="completed"
                appo.save()
                return redirect('doctorAppo')
            else:
                print("5")
                context={}
                context['data']=data
                context['appo']=appointmentconfirmation.objects.get(id=id)
                context['id']=id
                return render(request, 'doctor/moredetails.html',context)
        else:
            print("6")
            appo=appointmentconfirmation.objects.get(id=id)
            context={}
            context['data']=prescriptionForm()
            context['appo']=appo
            context['id']=id
            context['lab']=False
            print(context['lab'])
            return render(request, 'doctor/moredetails.html',context)
        


def viewreport(request, id):
    data=Prescription.objects.get(appoint_id=id)
    appo=appointmentconfirmation.objects.get(id=id)
    context={}
    context['data']=data
    context['appo']=appo
    if labReport.objects.filter(prescription_id=data.id).exists():
        lab=labReport.objects.get(prescription_id=data.id)
        context['lab']=lab
    return render(request, 'doctor/lab_details.html',context)
