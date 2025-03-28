
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Student  # Import your custom user model
from .models import Complaint

admin.site.register(Complaint)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_student', 'is_clerk', 'is_matron', 'is_warden')
    list_filter = ('is_student', 'is_clerk', 'is_matron', 'is_warden')
    
    fieldsets = UserAdmin.fieldsets + (
        ('User Roles', {'fields': ('is_student', 'is_clerk', 'is_matron', 'is_warden')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('User Roles', {'fields': ('is_student', 'is_clerk', 'is_matron', 'is_warden')}),
    )

# Custom Student Admin
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'admission_number', 'username', 'email', 'course', 'department', 'semester')
    search_fields = ('full_name', 'admission_number', 'username', 'email')
    list_filter = ('course', 'department', 'semester')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Student, StudentAdmin)