from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Doctor,Prescription
from accounts.models import Account
from patient.models import appointmentconfirmation

class UserForm(forms.ModelForm):
    class Meta:
        model=Account
        # exclude=['']
        fields=['first_name','last_name','state','district','contact','usr_img','dob','gender']

        widgets={
            'first_name':forms.TextInput(attrs={'class':'form-control','placeholder':'First Name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control','placeholder':'Last Name'}),
            'state':forms.Select(attrs={'class':'form-control','placeholder':'State'}),
            'district':forms.Select(attrs={'class':'form-control','placeholder':'District'}),
            'contact':forms.NumberInput(attrs={'class':'form-control','placeholder':'Contact'}),
            'usr_img':forms.FileInput(attrs={'class':'form-control','placeholder':'Image'}),
            'dob':forms.DateInput(attrs={'class':'form-control','placeholder':'Date of Birth'}),
            'gender':forms.Select(attrs={'class':'form-control','placeholder':'Enter Gender'}),
        }

class DoctorForm(forms.ModelForm):
    class Meta:
        model=Doctor
        fields=['spec_name','year_of_service','qual_name','license_no','des_name']
        widgets={
            'spec_name':forms.Select(attrs={'class':'form-control','placeholder':'specialization'}),
            'year_of_service':forms.NumberInput(attrs={'class':'form-control','placeholder':'Year of Service'}),
            'qual_name':forms.SelectMultiple(attrs={'class':'form-control','placeholder':'Qualification'}),
            'license_no':forms.TextInput(attrs={'class':'form-control','placeholder':'License No'}),
            'des_name':forms.Select(attrs={'class':'form-control','placeholder':'Designation'}),

        }

class appointmentForm(forms.ModelForm):

    class Meta:
        model=appointmentconfirmation
        fields=['appo_date','appo_time','appo_status','payment']

        def __init__(self,*args,**kwrgs):
            user=kwrgs.pop('user','')
            super(appointmentForm,self).__init__(*args,**kwrgs)
            self.fields['first_name']=forms.ModelChoiceField(queryset=Account.objects.filter(id=user),empty_label='Select First Name')
            self.fields['email']=forms.ModelChoiceField(queryset=Account.objects.filter(id=user),empty_label='Select email')
        
        widgets={
            'appo_date':forms.DateInput(attrs={'class':'form-control','placeholder':'Date of Birth'}),
            'appo_time':forms.TimeInput(attrs={'class':'form-control','placeholder':'Time'}),
            'appo_status':forms.Select(attrs={'class':'form-control','placeholder':'Status'}),
            'payment':forms.Select(attrs={'class':'form-control','placeholder':'Payment'}),
        }

class prescriptionForm(forms.ModelForm):
    class Meta:
        model=Prescription
        fields=['symptoms','diagnosis','prescription','lab_report']

        widgets={
            'prescription':forms.Textarea(attrs={'class':'form-control','placeholder':'Prescription','id':'inputbox'}),
            'symptoms':forms.Textarea(attrs={'class':'form-control','placeholder':'Symptoms','id':'inputbox'}),
            'diagnosis':forms.Textarea(attrs={'class':'form-control','placeholder':'Diagnosis','id':'inputbox'}),
            'lab_report':forms.Select(attrs={'class':'form-control','placeholder':'Lab Report','id':'inputbox'}),
            
        }

class prescriptionFormReadyonly(forms.ModelForm):
    class Meta:
        model=Prescription
        fields=['symptoms','diagnosis','prescription','lab_report']

        widgets={
            'prescription':forms.Textarea(attrs={'class':'form-control','placeholder':'Prescription','id':'inputbox','readonly':'readonly'}),
            'symptoms':forms.Textarea(attrs={'class':'form-control','placeholder':'Symptoms','id':'inputbox','readonly':'readonly'}),
            'diagnosis':forms.Textarea(attrs={'class':'form-control','placeholder':'Diagnosis','id':'inputbox','readonly':'readonly'}),
            'lab_report':forms.Select(attrs={'class':'form-control','placeholder':'Lab Report','id':'inputbox','readonly':'readonly'}),
        }

