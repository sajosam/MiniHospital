from django.shortcuts import render

# Create your views here.


def doctorHome(request):
    return render(request, 'doctor/doctorHome.html')