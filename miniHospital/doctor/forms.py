from dataclasses import fields
from pyexpat import model
from django import forms
from .models import Doctor
from accounts.models import Account

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
            # 'email':forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}),
            # 'password':forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}),
            # 'username':forms.TextInput(attrs={'class':'form-control','placeholder':'Username'}),
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

