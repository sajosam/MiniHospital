
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('', views.labHome, name='labhome'),
    path('update/',views.labUpdate, name='labUpdate'),
    path('viewAppo', views.labViewAppo, name='labViewAppo'),
    path('addreport/<int:id>', views.addreport, name='addreport'),
    
]
