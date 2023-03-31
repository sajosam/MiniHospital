from django.contrib import admin
from .models import leaveModel,datanalysis
from import_export.admin import ImportExportModelAdmin
from .models import demo

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


################################################################
################################################################
################################################################
################################################################
################################################################
################################################################
################################################################
# admin panel validation field validation

from django import forms
from django.contrib import admin
from .models import demo

class MyModelAdminForm(forms.ModelForm):
    class Meta:
        # models 
        model = demo
        fields = '__all__'

    def clean_name(self):
        cleaned_data = super().clean() #permanent
        name = cleaned_data.get('name')#field data
        if name == 'foo': #condition
            raise forms.ValidationError('name cannot be foo')
        # name is not number
        if name.isnumeric():
            raise forms.ValidationError('name is not number')
        
        return cleaned_data

class MyModelAdmin(admin.ModelAdmin):
    form = MyModelAdminForm

admin.site.register(demo, MyModelAdmin)
