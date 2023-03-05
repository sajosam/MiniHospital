# Sceduling Algorithm

from django.db import models
from .models import *
from doctor.models import *
from lab.models import *

class SchedulingAlgorithm:
    def __init__(self,d_email, date, time):
        # self.p_id = p_id
        self.d_email = d_email
        self.date = date
        self.time = time

    def schedule(self):
        print(self.d_email)
        print(self.date)
        print(self.time)

        FN_time=['10:00:00', '10:10:00', '10:20:00', '10:30:00', '10:40:00', '10:50:00', '11:00:00', '11:10:00', '11:20:00', '11:30:00','11:40:00','11:50:00', '12:00:00', '12:10:00', '12:20:00', '12:30:00','12:40:00', '12:50:00']
        AN_time=['02:00:00','02:10:00','02:20:00','02:30:00','02:40:00','02:50:00','03:00:00','03:10:00','03:20:00','03:30:00','03:40:00', '03:50:00']
        excluded_appo=patientAppointment.objects.filter(doc_email=self.d_email, date=self.date,leaveStatus=True).values_list('time', flat=True)
        
        print("ex",excluded_appo)
        strr=[str(i) for i in excluded_appo]
        print("de",strr)

        if self.time == 'FN':
            for time in FN_time:
                if time not in strr:
                    return time
        elif self.time == 'AN':
            for time in AN_time:
                if time not in strr:
                    return time
        else:
            return False
        





