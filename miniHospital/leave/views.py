from django.shortcuts import render
from django.shortcuts import redirect
from .models import leaveModel

# Create your views here.


def leave(request):
    ext=request.user.is_doctor
    data=leaveModel.objects.filter(email__email=request.user.email)
    context = {
        'ext': 'doctor/doctorBase.html' if ext else 'lab/labBase.html',
        'data': data
    }
    return render(request, 'leave/leave.html', context)

def leaveApply(request):
    if request.method == 'POST':
        leaveDate = request.POST['date']
        leaveDiv = request.POST['div']
        leaveReason = request.POST['reason']
        print(leaveDate)
        if leaveDiv=='FD':
            leaveDiv='AN, FN'
        leaveStatus = False
        email = request.user
        leaveModel.objects.create(email=email, leaveDate=leaveDate, leaveDiv=leaveDiv, leaveReason=leaveReason, leaveStatus=leaveStatus)
        return redirect('leave')
    ext=request.user.is_doctor
    context = {
        'ext': 'doctor/doctorBase.html' if ext else 'lab/labBase.html',
    }
    return render(request, 'leave/leaveApply.html', context)

