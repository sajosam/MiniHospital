
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.doctorHome, name='doctorHome'),
    path('update/',views.doctorUpdate, name='doctorUpdate'),
    path('viewAppo', views.doctorAppo, name='doctorAppo'),
    path('viewpatient/<int:id>', views.viewpatient, name='viewpatient'),
    path('viewreport/<int:id>', views.viewreport, name='viewreport'),
    
]
