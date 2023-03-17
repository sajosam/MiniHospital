import email
from django.db import models
from ckeditor.fields import RichTextField

from accounts.models import Account

class patientData(models.Model):
    blood_group=(
        ('A+','A+'),
        ('A-','A-'),
        ('B+','B+'),
        ('B-','B-'),
        ('AB+','AB+'),
        ('AB-','AB-'),
        ('O+','O+'),
        ('O-','O-'),
    )

    bool_select=(
        ('Yes','Yes'),
        ('No','No'),
    )
    id = models.AutoField(primary_key=True)
    user_id=models.ForeignKey(Account, on_delete=models.CASCADE,limit_choices_to={'is_patient':True})
    is_diabetic = models.CharField(default='No',max_length=25,choices=bool_select)
    is_asthma = models.CharField(default='No',max_length=25,choices=bool_select)
    is_hypertension = models.CharField(default='No',max_length=25,choices=bool_select)
    is_stroke= models.CharField(default='No',max_length=25,choices=bool_select)
    alergetic_drugs=RichTextField(max_length=250, blank=True)
    weight= models.FloatField(default=None, blank=True)
    height= models.FloatField(default=None, blank=True)
    is_alcoholic= models.CharField(default='No',max_length=25,choices=bool_select)
    blood_group=models.CharField(max_length=10, blank=True, choices=blood_group)
    covid_vacciantion=models.CharField(default='No',max_length=25,choices=bool_select)
    
class appointmentconfirmation(models.Model):
    status=(
        ('pending','pending'),
        ('accepted','accepted'),
        ('rejected','rejected'),
        ('completed','completed'),
        ('cancelled','cancelled'),
        ('rescheduled','rescheduled'),
        ('in_progress','in_progress'),
    )

    fee=(
        ('paid','paid'),
        ('unpaid','unpaid'),
    )
    id=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(Account, on_delete=models.CASCADE,limit_choices_to={'is_patient':True},related_name='user_email')
    doc_email=models.ForeignKey(Account, on_delete=models.CASCADE,related_name='doctor_email',limit_choices_to={'is_doctor':True})
    appo_date=models.DateField(default=None)
    appo_time=models.TimeField(default=None)
    appo_status=models.CharField(max_length=20, choices=status, default='pending')
    payment=models.CharField(max_length=20, choices=fee, default='unpaid')
    payment_id=models.ForeignKey('Payment', on_delete=models.CASCADE,blank=True,null=True)

    # def __str__(self):
    #     return self.user_id.email
    # return id
    def __str__(self):
        return str(self.id)


class Payment(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    amount = models.FloatField(blank=True,null=True)
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    appo_id=models.ForeignKey(appointmentconfirmation, on_delete=models.CASCADE,blank=True,null=True,related_name='appo_id')
    signature = models.CharField(max_length=100,blank=True,null=True)

    def __str__(self):
        return self.user.email
    