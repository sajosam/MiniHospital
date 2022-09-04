import re
from django.shortcuts import render
# from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.


def home(request):
    return render(request, 'patient/home.html')



def handler404(request,exception):
    return render(request, 'error/404.html')

