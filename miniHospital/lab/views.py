from django.shortcuts import render

# Create your views here.

def labHome(request):
    return render(request, 'lab/labHome.html')