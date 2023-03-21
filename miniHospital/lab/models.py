from django.db import models
from accounts.models import Account
from doctor.models import Specialization, Designation, Prescription
from multiselectfield import MultiSelectField
import datetime
from cloudinary.models import CloudinaryField


# from doctor.models import Prescription
from patient.models import appointmentconfirmation

# Create your models here.

class Lab(models.Model):
    qualification_names = (
        ('DMLT','DMLT'), #Diploma in Medical Laboratory Technology
        ('ADMLT','ADMLT'), #Associate in Medical Laboratory Technology
        ('BMLT','BMLT'), #Bachelor of Medical Laboratory Technology
        ('MLT','MLT'), #Medical Laboratory Technology
    )

    id = models.AutoField(primary_key=True)
    email = models.ForeignKey(Account, on_delete=models.CASCADE)
    year_of_service = models.IntegerField(blank=False, null=False)
    # qual_name = models.ForeignKey(Qualification, on_delete=models.CASCADE,related_name='q-realated')
    qual_name = MultiSelectField(choices=qualification_names, max_choices=5, max_length=100)
    spec_name = models.ForeignKey(Specialization, on_delete=models.CASCADE,related_name='spec_name_realted')
    des_name = models.ForeignKey(Designation, on_delete=models.CASCADE,related_name='des_name_lab')
    license_no = models.CharField(max_length=100, blank=True)
    is_doctor = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_lab = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.email.first_name


class labReport(models.Model):
    lab_type=(
        ('Blood','Blood'),
        ('Urine','Urine'),
        ('Stool','Stool'),
        ('Sputum','Sputum'),
        ('X-Ray','X-Ray'),
        ('CT-Scan','CT-Scan'),
        ('MRI','MRI'),
        ('ECG','ECG'),
        ('Ultrasound','Ultrasound'),
        ('Other','Other'),
    )
    status_choice=(
        ('Pending','Pending'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),
        ('Rejected','Rejected'),
        ('Accepted','Accepted'),
        ('In Progress','In Progress'),
    )
    
    id = models.AutoField(primary_key=True)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE,blank=True, null=True)
    patient = models.ForeignKey(Account, on_delete=models.CASCADE,limit_choices_to={'is_patient': True})
    appoint_id=models.ForeignKey(appointmentconfirmation, on_delete=models.CASCADE)
    prescription_id=models.ForeignKey(Prescription, on_delete=models.CASCADE,blank=True, null=True)
    report = models.FileField(upload_to='lab_report/', blank=True, null=True)
    date = models.DateField(default=datetime.date.today)
    lab_uidd=models.IntegerField(blank=True, null=True)
    status=models.CharField(max_length=100, choices=status_choice,default='In Progress')

    def __str__(self):
        return self.patient.first_name

    
    
