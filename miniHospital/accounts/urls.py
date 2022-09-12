
from django.urls import path, include
from . import views
from django.contrib import admin


urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),

]
