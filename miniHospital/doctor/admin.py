
import re
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Doctor, Designation, Specialization,Prescription
from import_export.admin import ImportExportModelAdmin
# Register your models here.


class DoctorAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    # disply profile image from another foregin table
    def pro(self, obj):
        # return obj.email.usr_img.url
        if obj.email.usr_img.url:
            return format_html('<img src="{}" width="100" style="border-radius : 20px;" />'.format(obj.email.usr_img.url))
        else:
            return format_html('<img src="https://res.cloudinary.com/mini-hospital/image/upload/v1663391619/man_vtqh4u.png" width="100" style="border-radius : 20px;" />')


    def f_name(self,object):
        return object.email.first_name
    
    def l_name(self,object):
        return object.email.last_name
    
    def date_last_updated(self,object):
        return object.email.last_login

    list_display = ('pro','email','f_name','l_name','year_of_service','qual_name','spec_name','des_name','license_no','is_active','date_last_updated')
    list_display_links = ('email',)
    # readonly_fields = ('last_login', 'date_joined')
    # ordering = ('-date_joined',)
    # filter_horizontal = 'qual_name']
    list_filter = ['year_of_service','qual_name','spec_name']
    fieldsets = ()

    
admin.site.register(Doctor, DoctorAdmin)


class DesignationAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('des_name',)
    list_display_links = ('des_name',)
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ['des_name']
    fieldsets = ()

admin.site.register(Designation, DesignationAdmin)


class SpecializationAdmin(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('spec_name',)
    list_display_links = ('spec_name',)
    readonly_fields = ()
    # filter_horizontal = ()
    filter_horizontal = ()

    list_filter = ['spec_name']
    fieldsets = ()

admin.site.register(Specialization, SpecializationAdmin)

admin.site.register(Prescription)

