
from django import forms
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

