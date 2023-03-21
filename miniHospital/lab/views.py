import email
from operator import ge
from pydoc import doc
from django.shortcuts import render, redirect
from accounts.models import Account
from .models import Lab, labReport
from datetime import date
from doctor.models import Doctor, Prescription
from .forms import LabForm, UserForm
from patient.models import appointmentconfirmation
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def labHome(request):
    if request.user.is_authenticated:
        if request.user.is_lab:
            email = request.session.get('email')
            print(email)
            # access details of lab in account table
            usr=Account.objects.get(email=email)
            # access profile details in lab tablet
            lab=Lab.objects.get(email__id=usr.id)

            context = {
                'lab': lab,
                'usr':usr,
                'exp':date.today().year-lab.year_of_service,
            }
            return render(request, 'lab/l-profile.html', context)
        else:
            return redirect('login')
    return redirect('login')
            

@login_required(login_url='login')
def labUpdate(request):
    usr=Account.objects.get(email=request.session.get('email'))
    lab=Lab.objects.get(email__id=Account.objects.get(email=request.session.get('email')).id)
    if request.method == 'GET':
        context={}
        context['usr_form']= UserForm(instance=Account.objects.get(email=request.session.get('email')))
        context['l_form']= LabForm(instance=Lab.objects.get(email__id=Account.objects.get(email=request.session.get('email')).id))
        context['usr']=usr
        context['lab']=lab
        return render(request, 'lab/l-update.html', context)
    else:
        form = UserForm(request.POST, request.FILES)
        lab_form = LabForm(request.POST)
        # 
        if form.is_valid() and lab_form.is_valid():
            # email = request.session.get('email')
            usr=Account.objects.get(email=request.session.get('email'))
            usr.first_name = form.cleaned_data['first_name']
            usr.last_name = form.cleaned_data['last_name']
            usr.state = form.cleaned_data['state']
            usr.district = form.cleaned_data['district']
            usr.contact = form.cleaned_data['contact']
            usr.usr_img = form.cleaned_data['usr_img']
            
            usr.dob = form.cleaned_data['dob']
            usr.save()
            l=Lab.objects.get(email__id=usr.id)
            l.spec_name = lab_form.cleaned_data['spec_name']
            l.year_of_service = lab_form.cleaned_data['year_of_service']
            l.qual_name = lab_form.cleaned_data['qual_name']
            l.license_no = lab_form.cleaned_data['license_no']
            l.des_name = lab_form.cleaned_data['des_name']
            l.save()
            return redirect('labhome')
        else:
            context={}
            context['form']= form
            context['lab_form']= lab_form
            context['usr']=usr
            context['lab']=lab
            return render(request, 'lab/l-update.html', context)


def labViewAppo(request):
    # extract appointment basewd on same department
    lab=Lab.objects.get(email__id=request.user.id)
    appo=Doctor.objects.filter(spec_name=lab.spec_name).values_list('email_id', flat=True)
    lst=[x for x in appo]
    data=appointmentconfirmation.objects.filter(doc_email__in=lst).values_list('id',flat=True)
    print(data)
    dat=Prescription.objects.filter(appoint_id__in=data).values_list('id',flat=True)
    print(dat)
    da=labReport.objects.filter(prescription_id__in=dat)
    print(da)
    
    context={
        'data':data,
        'dat':dat,
        'da':da,
    }

    return render(request, 'lab/viewappo.html', context)

def addreport(request, id):
    data=labReport.objects.get(id=id)
    if request.method == 'POST':
        report=request.POST.get('report')
        print(report)
        data.report=report
        data.lab=Lab.objects.get(email__id=request.user.id)
        data.status='Completed'
        data.save()
        return redirect('labViewAppo')
    else:
        context={
            'data':data,
        }
    return render(request, 'lab/viewreport.html', context)