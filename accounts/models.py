from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    is_student = models.BooleanField('Is Student', default=False)
    is_clerk = models.BooleanField('Is Clerk', default=False)
    is_matron = models.BooleanField('Is Matron', default=False)
    is_warden = models.BooleanField('Is Warden', default=False)

class Student(models.Model):
    #personal details
    full_name = models.CharField(max_length=255)
    admission_number = models.CharField(max_length=50, unique=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    age = models.IntegerField()
    aadhar_number = models.CharField(max_length=12, unique=True)
    mobile_number = models.CharField(max_length=12)
    religion = models.CharField(max_length=50)
    caste = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    annual_income = models.DecimalField(max_digits=10, decimal_places=2)

    
    course = models.CharField(max_length=50)
    department = models.CharField(max_length=100)
    semester = models.CharField(max_length=20)
    
    address = models.TextField( blank=True)
    pincode = models.IntegerField()
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    nationality = models.CharField(max_length=50)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    # Father's Details
    father_name = models.CharField(max_length=100)
    father_occupation = models.CharField(max_length=100, blank=True)
    father_addresss = models.CharField(max_length=100)
    father_mobile = models.CharField(max_length=15)
    father_email = models.EmailField(max_length=50)

    mother_name = models.CharField(max_length=100, blank=True)
    mother_occupation = models.CharField(max_length=100, blank=True)
    mother_addresss = models.CharField(max_length=100, blank=True)
    mother_mobile = models.CharField(max_length=15,blank=True)
    mother_email = models.EmailField(max_length=50,blank=True)

    # Guardian's Details
    guardian_name = models.CharField(max_length=255)
    guardian_addresss = models.CharField(max_length=100)
    guardian_occupation = models.CharField(max_length=255, blank=True)
    guardian_mobile = models.CharField(max_length=15)
    guardian_email = models.EmailField(max_length=50)

    
    
    # Upload Documents
    ration_document = models.FileField(upload_to='documents/ration/', null=True, blank=True)
    aadhar_document = models.FileField(upload_to='documents/aadhar/', null=True, blank=True)
    income_certificate = models.FileField(upload_to='documents/income/', null=True, blank=True)
    caste_documents = models.FileField(upload_to='documents/caste/', null=True, blank=True)
class Complaint(models.Model):
    CATEGORY_CHOICES = [
        ('Hostel Facility', 'Hostel Facility'),
        ('Mess', 'Mess'),
        ('Students', 'Students'),
        ('Staff', 'Staff'),
        ('Others', 'Others'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Resolved', 'Resolved'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)  
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField()
    file = models.FileField(upload_to='complaints_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        # Check if the user exists before trying to access username
        if self.user:
            return f"Complaint by {self.user.username} - {self.category} ({self.status})"
        return f"Complaint - {self.category} ({self.status})"  # Default return if no user

class MessCommittee(models.Model):
    students = models.ManyToManyField('Student')  # Multiple students in a committee
    month = models.CharField(max_length=20)  # e.g., "March", "April"
    year = models.IntegerField()  # e.g., 2025

    class Meta:
        unique_together = ("month", "year")  # Ensure only one committee per month-year

    def __str__(self):
        return f"Mess Committee - {self.month} {self.year}"
