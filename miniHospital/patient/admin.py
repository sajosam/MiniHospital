from django.contrib import admin
from .models import patientData,appointmentconfirmation
from import_export.admin import ImportExportModelAdmin
# Register your models here.


# admin.site.register(PatientData)
# admin.site.register(patientAppointment)

@admin.register(patientData)
class PatientDataAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    def first_name(self,object):
        return object.user_id.first_name
    def last_name(self,object):
        return object.user_id.last_name
    def email(self,object):
        return object.user_id.email
    

    list_display = ('id','first_name','last_name','email')
    readonly_fields = ('id','first_name','last_name','email')


@admin.register(appointmentconfirmation)
class AppointmentAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    
    def DoctorName(self,object):
        return object.doc_email.first_name+" "+object.doc_email.last_name
    
    def PatientName(self,object):
        return object.user_id.first_name+" "+object.user_id.last_name
    
    def PatientEmail(self,object):
        return object.user_id.email
    
    list_display = ('id','DoctorName','PatientName','PatientEmail','appo_date','appo_time','status')
    readonly_fields = ('id','DoctorName','PatientName','PatientEmail','appo_date','appo_time','status')



