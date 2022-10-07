from django.contrib import admin
from .models import PatientData, appointment
# Register your models here.


admin.site.register(PatientData)
admin.site.register(appointment)