from django.shortcuts import render, redirect
from django.core.signing import Signer
from django.contrib import messages
from .models import Student
from datetime import datetime

# Create your views here.
def register(request):
    enc_data = None
    if request.method == 'POST':
        sname = request.POST['name']
        sroll = request.POST['roll']
        sbirth = request.POST['birth']
        session_1st = request.POST['1st_session']
        session_2nd = request.POST['2nd_session']
        shift = request.POST['shift']
        exist = Student.objects.filter(roll=sroll).exists()
        if exist:
            messages.error(request, "Student already Exist in database")
            
        else:
            stud = Student.objects.create(name=sname, roll=sroll, birth_date=sbirth, shift=shift, session=f"{session_1st} to {session_2nd}")
            stud.save()
            s = Signer()
            enc_data = s.sign_object({sroll: sbirth})
            messages.success(request, "Student added in database")
    return render(request, "register.html", {'data': enc_data})

def login(request):
    if request.method == 'POST':
        roll = request.POST.get("roll")
        birth = request.POST.get("dateofbirth")
        if student:=student_authenticate(roll, birth):
            s = Signer()
            enckey = s.sign_object({roll:birth})
            return redirect('dashboard', pk=enckey)
            #TODO: redirect with encrypted roll and birthdate
    
    return render(request, "login.html")

def student_authenticate(roll=None, birth=None):
        try:
            student = Student.objects.get(roll = roll)
        except ValueError as e:
            print(e)
        except Student.DoesNotExist as e:
            print(e)

        else:
            if datetime.strftime(student.birth_date, "%Y-%m-%d") == birth:
                return student
            else:
                return False

def dashboard(request, pk):
    s = Signer()
    roll_birth = s.unsign_object(pk)
    roll, birth = tuple(roll_birth.items())[0]
    
    return render(request, 'dashboard.html',{'student':{'name':birth, "roll":roll}, "qr_data":pk})