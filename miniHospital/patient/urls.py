
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='patientHome'),
    path('profile/', views.patient, name='patientProfile'),
    path('patientUpdate/',views.patientUpdate, name='patientUpdate'),
    path('checkavailability/',views.checkavailability, name='checkavailability'),
    path('patientData/',views.patientData, name='patientData'),
    path('doc_list/',views.doc_list, name='doc_list'),
    path('singleDoc/<int:id>', views.singleDoc, name='singleDoc'),
    path('availability/', views.availability, name='availability'),
    # path('appointment/<int:id>/', views.appointment, name='appointment'),
    # path('appointment/', views.appointment, name='appointment'),
    path('appointment/<str:time>/', views.appointment, name='appointment'),
    path('viewappointments/',views.viewappointments, name='viewappointments'),
    path('confirmappointment/', views.confirmappointment, name='confirmappointment'),
    path('availspec/<int:id>/', views.availspec, name='availspec'),
    path('availdoc/<int:id>/', views.availdoc, name='availdoc'),
    path('availability/', views.availability, name='availability'),
    path('viewpatientappo/', views.viewpatientappo, name='viewpatientappo'),
    path('cancelappointment/<int:id>/', views.cancelappointment, name='cancelappointment'),
    path('reschedule/<int:id>/', views.reschedule, name='reschedule'),
    path('rescheduleappointment/<str:time>/<int:id>', views.rescheduleappointment, name='rescheduleappointment'),
    path('rescheduletime/', views.rescheduletime, name='rescheduletime'),
    

]
