
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='patientHome'),
    path('profile/', views.patient, name='patientProfile'),
    path('patientUpdate/',views.patientUpdate, name='patientUpdate')
]
