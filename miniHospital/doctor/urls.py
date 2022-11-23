
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.doctorHome, name='doctorHome'),
    path('update/',views.doctorUpdate, name='doctorUpdate'),
    path('viewAppo', views.doctorAppo, name='doctorAppo'),
]
