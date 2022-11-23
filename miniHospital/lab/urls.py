
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.labHome, name='labhome'),
    path('update/',views.labUpdate, name='labUpdate'),
    path('viewAppo', views.labViewAppo, name='labViewAppo'),
]
