from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from django import forms

# Register your models here.


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from import_export.admin import ImportExportModelAdmin
from .models import Account
from . import forms


class AccountAdmin(ImportExportModelAdmin, UserAdmin):
    # form = forms.MyModelAdmin
    def thumbnail(self, object):
        if object.usr_img:
            return format_html('<img src="{}" width="100" style="border-radius : 20px;" />'.format(object.usr_img.url))
        else:
            return format_html('<img src="https://res.cloudinary.com/mini-hospital/image/upload/v1663391619/man_vtqh4u.png" width="100" style="border-radius : 20px;" />')



    thumbnail.short_description="Photo"
    list_display = ('id','thumbnail','email', 'first_name', 'last_name', 'username','state','district','dob','gender', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email','thumbnail')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ['last_login', 'date_joined', 'is_active','is_admin','is_lab','is_doctor','is_patient']
    fieldsets = ()
    # list_editable=['first_name','last_name']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'state', 'district', 'dob', 'gender', 'is_active', 'is_admin', 'is_lab', 'is_doctor', 'is_patient')}
        ),
    )
    
admin.site.register(Account, AccountAdmin)


