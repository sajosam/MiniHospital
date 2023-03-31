from django.db import models
from accounts.models import Account
from doctor.models import Doctor

# Create your models here.


class leaveModel(models.Model):
    leave_choices = (
        ('FN', 'FN'),
        ('AN', 'AN'),
        ('FD', 'FD'),
        ('None', 'None'),
    )
    leaveId = models.AutoField(primary_key=True)
    email = models.ForeignKey(Account, on_delete=models.CASCADE)
    leaveDate = models.DateField()
    leaveDiv= models.CharField(max_length=10)
    leaveReason = models.CharField(max_length=50)
    leaveStatus = models.BooleanField('Approved',default=False)
    

    # def __str__(self):
    #     return self.email\


class datanalysis(models.Model):
    id = models.AutoField(primary_key=True)
    age= models.IntegerField()
    gender= models.CharField(max_length=20)
    month= models.CharField(max_length=20)
    time=models.CharField(max_length=20)
    day= models.CharField(max_length=20)
    day_type= models.CharField(max_length=20)
    specialty= models.CharField(max_length=20)
    disease= models.CharField(max_length=100)


class demo(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    def __str__(self):
        return self.name