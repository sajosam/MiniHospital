
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
    path('appointment/<int:id>/', views.appointment, name='appointment'),
    path('viewappointments/',views.viewappointments, name='viewappointments'),
    path('confirmappointment/', views.confirmappointment, name='confirmappointment'),
    path('chat/', views.diagnosis_view, name='chat'),
    # path('chatroom/', views.chatbot_view, name='chatroom'),

]
