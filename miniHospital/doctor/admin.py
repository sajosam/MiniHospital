

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Doctor, Designation, Specialization
# Register your models here.


class DoctorAdmin(admin.ModelAdmin):
    list_display = ('email','is_active','year_of_service','qual_name','spec_name','des_name','license_no')
    list_display_links = ('email',)
    # readonly_fields = ('last_login', 'date_joined')
    # ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

    
admin.site.register(Doctor, DoctorAdmin)


class DesignationAdmin(admin.ModelAdmin):
    list_display = ('des_name',)
    list_display_links = ('des_name',)
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Designation, DesignationAdmin)


class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('spec_name',)
    list_display_links = ('spec_name',)
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(Specialization, SpecializationAdmin)


