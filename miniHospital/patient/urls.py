
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='patientHome'),
    path('profile/', views.patient, name='patientProfile'),
    path('patientUpdate/',views.patientUpdate, name='patientUpdate'),
    path('appointment/',views.Appointment, name='appointment'),
    path('patientData/',views.patientData, name='patientData'),
    path('doc_list/',views.doc_list, name='doc_list'),
]
