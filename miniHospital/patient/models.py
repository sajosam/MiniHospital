import email
from django.db import models
from ckeditor.fields import RichTextField

from miniHospital.accounts.models import Account

# Create your models here.

class PatientData(models.Model):

    # drug choices
    drug=(
        ('Penicillin','Penicillin'),
        ('Amoxicillin','Amoxicillin'),
        ('Azithromycin','Azithromycin'),
        ('Ciprofloxacin','Ciprofloxacin'),
        ('Levofloxacin','Levofloxacin'),
        ('Metronidazole','Metronidazole'),
        ('Clindamycin','Clindamycin'),
        ('Erythromycin','Erythromycin'),
        ('Tetracycline','Tetracycline'),
        ('Doxycycline','Doxycycline'),
        ('Ceftriaxone','Ceftriaxone'),
        ('Cefuroxime','Cefuroxime'),
        ('Cefixime','Cefixime'),
        ('Cefpodoxime','Cefpodoxime'),
        ('Cefdinir','Cefdinir'),
        ('Cefaclor','Cefaclor')
    )
    id = models.AutoField(primary_key=True)
    email=models.ForeignKey(Account, on_delete=models.CASCADE)
    is_diabetic = models.BooleanField(default=False)
    is_asthma = models.BooleanField(default=False)
    is_hypertension = models.BooleanField(default=False)
    is_stroke= models.BooleanField(default=False)
    alergetic_drugs=models.CharField(max_length=50,choices=drug)
    weight= models.FloatField(default=None, blank=True)
    height= models.FloatField(default=None, blank=True)
    is_alcoholic= models.BooleanField(default=False)
    symptoms=RichTextField()


# class appointment(models.Model):
#     id= models.AutoField(primary_key=True)
#     email= models.ForeignKey(Account, on_delete=models.CASCADE)
