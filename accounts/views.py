from django.shortcuts import render,redirect
from .forms import SignUpForm, LoginForm, StudentForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Student
from .models import Complaint
from .forms import ComplaintForm
# Create your views here.
def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
           
            if user.is_student:
                return redirect('student_data')
            else:
                return redirect('login')
            
        else:
            msg = 'form is not valid'
    else :
        form = SignUpForm()
    return render(request, 'registration/register.html', {'form' : form, 'msg' : msg})

def student_data(request):
    if request.method == 'POST':
        print("Received POST data:", request.POST)
        form = StudentForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid") 
            form.save()
            return redirect('login')
        else:
            print("Form errors:", form.errors) 
    form = StudentForm()
    dict_form={
        'form' : form
    }
    return render(request, 'registration/student_data.html',dict_form)

def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    next_url = request.GET.get('next')  # Get next URL if available

    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                
                if next_url:  
                    return redirect(next_url)  # Redirect to intended page
                
                # Role-based redirection
                if hasattr(user, 'is_student') and user.is_student:
                    return redirect('student')
                elif hasattr(user, 'is_clerk') and user.is_clerk:
                    return redirect('clerk')
                elif hasattr(user, 'is_warden') and user.is_warden:
                    return redirect('warden')
                elif hasattr(user, 'is_matron') and user.is_matron:
                    return redirect('matron')
                else:
                    return redirect('/')  # Default redirect

            else:
                msg = 'Invalid credentials'
        else:
            msg = 'Error validating form'
    
    return render(request, 'registration/login.html', {'form': form, 'msg': msg})

def logout_view(request):
    """Handles user logout."""
    logout(request)
    return redirect("home")

@login_required
def student(request):
    student = Student.objects.get(username=request.user.username) 
    return render(request, 'registration/student.html',{'student': student})

@login_required           
def clerk(request):
    return render(request, 'registration/clerk.html',{
        'Students':Student.objects.all()
    })
        

@login_required
def warden(request):
    return render(request, 'registration/warden.html')

@login_required
def matron(request):
    return render(request, 'registration/matron.html')

@login_required
def profile_view(request):
    student = Student.objects.get(username=request.user.username)  # Fetch student using registration number
    #complaints = Complaint.objects.filter(student=student).order_by('-timestamp')

    if request.method == "POST":
        form = StudentForm(request.POST, request.FILES, instance=student)  # Include FILES if profile pic is updated
        if form.is_valid():
            form.save()
            return redirect('student_profile')  # Redirect to profile page after saving
        else:
            print(form.errors)  
    return render(request, 'dashboard/student_profile.html',{'student': student})

@login_required
def attendance_view(request):
    return render(request, 'dashboard/student_attendance.html')

@login_required
def mess_view(request):
    return render(request, 'dashboard/student_mess.html')

@login_required
def payment_view(request):
    return render(request, 'dashboard/student_payment.html')

@login_required
def student_messcom(request):
    return render(request,'dashboard/student_messcom.html')

@login_required
def warden_committe(request):
    return render(request,'dashboard/warden_committe.html')


@login_required
def warden_complaint(request):
    return render(request,'dashboard/warden_complaint.html')

@login_required
def complaint_system(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('student_complaint')
    else:
        form = ComplaintForm()

    complaints = Complaint.objects.all()
    
    return render(request, 'dashboard/student_complaint.html', {'form': form, 'complaints': complaints})
