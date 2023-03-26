from django.contrib import admin
from .models import leaveModel,datanalysis
from import_export.admin import ImportExportModelAdmin


# Register your models here.

class adminLeaveModel(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('leaveId','email','leaveDiv','leaveDate','leaveReason','leaveStatus')
    list_display_links = ('email',)
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ['leaveDate','leaveStatus','leaveDiv']
    fieldsets = ()
    # editable fields
    list_editable  = ('leaveStatus',)

class admindataanalysis(ImportExportModelAdmin,admin.ModelAdmin):
    list_display = ('id','age','gender','month','time','day','day_type','specialty','disease')
    list_display_links = ('id',)
    readonly_fields = ()
    filter_horizontal = ()
    list_filter = ['month','time','day','day_type','specialty','disease']
    fieldsets = ()
    # editable fields
    list_editable  = ('age','gender','month','time','day','day_type','specialty','disease')

admin.site.register(datanalysis, admindataanalysis)


admin.site.register(leaveModel, adminLeaveModel)
