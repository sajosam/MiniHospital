
from django.urls import path, include
from . import views
from django.contrib import admin


urlpatterns = [
    path('', views.HomeView.as_view(),name='visualdash'),
    path('api', views.ChartData.as_view()),
    path('weekday',views.WeekdayView.as_view(),name='weekday'),
    path('api/weekday', views.WeekdayData.as_view()),
    path('gender',views.GenderView.as_view(),name='gender'),
    path('api/gender', views.GenderData.as_view()),
    path('api/age', views.AgeData.as_view()),
    path('age', views.AgeView.as_view(),name='age'),
    path('disease', views.DiseaseView.as_view(),name='disease'),
    path('api/disease', views.DiseaseData.as_view()),
    path('riskanalysis', views.RiskAnalysisView.as_view(),name='riskanalysis'),
    path('api/riskanalysis', views.RiskAnalysisData.as_view()),
]
