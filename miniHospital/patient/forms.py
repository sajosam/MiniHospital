
from django import forms
from accounts.models import Account
from .models import patientData


class UserForm(forms.ModelForm):
    class Meta:
        model=Account
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

class patientDataForm(forms.ModelForm):

    class Meta:
        model=patientData
        # exclude=['']
    

        fields=['is_diabetic','is_asthma','is_hypertension','is_stroke','alergetic_drugs','weight','height','is_alcoholic','blood_group','covid_vacciantion']

        widgets={
            'is_diabetic':forms.Select(attrs={'class':'form-control','placeholder':'Diabetic'}),
            'is_asthma':forms.Select(attrs={'class':'form-control','placeholder':'Asthma'}),
            'is_hypertension':forms.Select(attrs={'class':'form-control','placeholder':'Hypertension'}),
            'is_stroke':forms.Select(attrs={'class':'form-control','placeholder':'Stroke'}),
            'alergetic_drugs':forms.TextInput(attrs={'class':'form-control','placeholder':'Alergetic Drugs'}),
            'weight':forms.NumberInput(attrs={'class':'form-control','placeholder':'Weight'}),
            'height':forms.NumberInput(attrs={'class':'form-control','placeholder':'Height'}),
            'is_alcoholic':forms.Select(attrs={'class':'form-control','placeholder':'Alcoholic'}),
            'blood_group':forms.Select(attrs={'class':'form-control','placeholder':'Blood Group'}),
            'covid_vacciantion':forms.Select(attrs={'class':'form-control','placeholder':'Covid Vacciantion'}),
            
        }