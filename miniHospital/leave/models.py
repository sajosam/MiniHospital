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
    #     return self.email