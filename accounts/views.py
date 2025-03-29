from django.shortcuts import render,redirect
from .forms import SignUpForm, LoginForm,ComplaintForm, StudentForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .models import Student,Complaint,MessCommittee
import random,datetime
from django.http import HttpResponse
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
    student = Student.objects.filter(username=request.user.username).first()  # Avoids exception
    if not student:
        return HttpResponse("Student not found", status=404)  # Handle missing student case

    return render(request, 'registration/student.html', {'student': student})

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
    current_month = datetime.datetime.now().strftime("%B")
    current_year = datetime.datetime.now().year

    # Fetch the subcommittee for the current month and year
    subcommittee = MessCommittee.objects.filter(month=current_month, year=current_year).first()

    # Fetch students in the subcommittee if it exists
    students_in_committee = subcommittee.students.all() if subcommittee else []

    return render(request, "dashboard/student_messcom.html", {
        "students_in_committee": students_in_committee,
        "month": current_month,
        "year": current_year
    })


    


@login_required
def warden_committe(request):
    current_month = datetime.datetime.now().strftime("%B")
    current_year = datetime.datetime.now().year

    # Get last month's details
    last_month = (datetime.datetime.now().replace(day=1) - datetime.timedelta(days=1)).strftime("%B")
    last_year = current_year if last_month != "December" else current_year - 1

    # Check if a committee exists for this month
    existing_committee = MessCommittee.objects.filter(month=current_month, year=current_year).first()

    if not existing_committee:
        # Fetch all students
        students = list(Student.objects.all())

        # Get students from last month's committee
        last_month_committee = MessCommittee.objects.filter(month=last_month, year=last_year).values_list("students", flat=True)

        # Filter students who were NOT in last month's committee
        eligible_students = [student for student in students if student.id not in last_month_committee]

        if len(eligible_students) < 10:
            return render(request, "dashboard/warden_committe.html", {
                "error": "Not enough new students available!",
                "month": current_month,
                "year": current_year
            })

        # Shuffle and select 10 students
        random.shuffle(eligible_students)
        selected_students = eligible_students[:10]

        # Create a new committee
        existing_committee = MessCommittee.objects.create(month=current_month, year=current_year)
        existing_committee.students.set(selected_students)

    # Retrieve selected students
    committee_students = existing_committee.students.all()

    return render(request, "dashboard/warden_committe.html", {
        "committee": committee_students,
        "month": current_month,
        "year": current_year
    })

@login_required
def warden_complaint(request):
    complaints = Complaint.objects.all()
    if request.method == 'POST':
        complaint_id = request.POST.get('complaint_id')
        new_status = request.POST.get('status')
        
        try:
            complaint = Complaint.objects.get(id=complaint_id)
            complaint.status = new_status
            complaint.save()
        except Complaint.DoesNotExist:
            pass
        
        return redirect('warden_complaint')
    return render(request,'dashboard/warden_complaint.html',{'complaints': complaints})

@login_required
def complaint_system(request):
    if request.method == "POST":
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save(commit=False)  # Don't save yet
            complaint.user = request.user  # Assign the current logged-in user
            complaint.save()
            return redirect('student_complaint')
    else:
        form = ComplaintForm()

    complaints = Complaint.objects.filter(user=request.user)
    
    return render(request, 'dashboard/student_complaint.html', {'form': form, 'complaints': complaints})

@login_required
def matron_messcom(request):
    current_month = datetime.datetime.now().strftime("%B")
    current_year = datetime.datetime.now().year

    # Fetch the subcommittee for the current month and year
    subcommittee = MessCommittee.objects.filter(month=current_month, year=current_year).first()

    # Fetch students in the subcommittee if it exists
    students_in_committee = subcommittee.students.all() if subcommittee else []

    return render(request, "dashboard/matron_messcom.html", {
        "students_in_committee": students_in_committee,
        "month": current_month,
        "year": current_year
    })