from django.contrib import admin
from .models import leaveModel
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



admin.site.register(leaveModel, adminLeaveModel)