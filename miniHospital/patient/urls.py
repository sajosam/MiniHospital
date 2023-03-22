
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='patientHome'),
    path('profile/', views.patient, name='patientProfile'),
    path('viewpatientappo/', views.viewpatientappo, name='viewpatientappo'),
    path('patalldetailsupdate/',views.patalldetailsupdate, name='patalldetailsupdate'),
    path('checkavailability/',views.checkavailability, name='checkavailability'),
    path('doc_list/',views.doc_list, name='doc_list'),
    path('singleDoc/<int:id>', views.singleDoc, name='singleDoc'),
    path('availspec/<int:id>/', views.availspec, name='availspec'),
    path('availdoc/<int:id>/', views.availdoc, name='availdoc'),
    path('availability/', views.availability, name='availability'),
    path('appointment/<str:time>/', views.appointment, name='appointment'),
    path('confirmappointment/', views.confirmappointment, name='confirmappointment'),
    path('cancelappointment/<int:id>/', views.cancelappointment, name='cancelappointment'),
    path('reschedule/<int:id>/', views.reschedule, name='reschedule'),
    path('rescheduletime/', views.rescheduletime, name='rescheduletime'),
    path('rescheduleappointment/<str:time>/<int:id>', views.rescheduleappointment, name='rescheduleappointment'),

    path('payonline/<int:id>/', views.payonline, name='payonline'),
    path('viewPatReport/', views.patReport,name='viewPatReport'),
    path('viewPresc/', views.Viewpresc, name='viewPresc')



    # path('patientUpdate/',views.patientUpdate, name='patientUpdate'),

    
    # path('patientData/',views.patientDataview, name='patientData'),
    # path('viewappointments/',views.viewappointments, name='viewappointments'),
    # path('availability/', views.availability, name='availability'),
    # path('patData/',views.patientDataView, name='patData'),
    # path('patDataUpdate/',views.patDataUpdateView, name='patDataUpdate'),
    # path('appointmentconfirmation/',views.appointmentConfirmationView, name='appointmentConfirmation'),
    

]
