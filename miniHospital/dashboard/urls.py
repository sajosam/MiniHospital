
from django.urls import path, include
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.HomeView.as_view(),name='visualdash'),
    path('api', views.ChartData.as_view()),
]
