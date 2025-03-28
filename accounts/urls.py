from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout/',views.logout_view,name='logout'),
    path('clerk/',views.clerk,name='clerk'),
    path('warden/',views.warden,name='warden'),
    path('matron/',views.matron,name='matron'),
    path('student_data/',views.student_data,name='student_data'),   
    path('student/',views.student,name='student'), 
    path('profile/', views.profile_view, name='student_profile'),
    path('attendance/', views.attendance_view, name='student_attendance'),
    path('mess/', views.mess_view, name='student_mess'),
    path('payment/', views.payment_view, name='student_payment'),
    path('complaint/', views.complaint_system, name='student_complaint'),
]