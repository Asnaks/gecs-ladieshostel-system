from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models  import User, Student
from datetime import date
from .models import Complaint

class LoginForm(forms.Form):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                "class" : 'form-control'
            }
        )
    )

    password = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                "class" : 'form-control'
            }
        )
    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                "class" : 'form-control'
            }
        )
    )
    password1 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                "class" : 'form-control'
            }
        )
    )
    password2 = forms.CharField(
        widget = forms.PasswordInput(
            attrs = {
                "class" : 'form-control'
            }
        )
    )
    email = forms.CharField(
        widget = forms.TextInput(
            attrs = {
                "class" : 'form-control'
            }
        )
    )

    class Meta :
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_student', 'is_clerk', 'is_matron', 'is_warden')
    

class DateInput(forms.DateInput):
    input_type = 'date'

class StudentForm(forms.ModelForm):
    RELIGION_CHOICES = [
        ("Muslim", "Islam"),
        ("Hindu", "Hindu"),
        ("Christian", "Christian"),
        ("Others", "Others"),
    ]
    CASTE_CHOICES = [
        ("General", "General"),
        ("OBC", "OBC"),
        ("OEC", "OEC"),
        ("SC", "SC"),
        ("ST", "ST"),
    ]
    CATEGORY_CHOICES = [
        ("APL", "APL"),
        ("BPL", "BPL"),
    ]
    
    religion = forms.ChoiceField(choices=RELIGION_CHOICES, widget=forms.Select(), required=True)
    caste = forms.ChoiceField(choices=CASTE_CHOICES, widget=forms.Select(), required=True)
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, widget=forms.Select(), required=True)

    dob = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'id': 'dob',  # Add this to ensure JS can find it
                'max': date.today().strftime('%Y-%m-%d')  # Prevent future dates
            }
        )
    )

    age = forms.IntegerField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        required=False
    )
    class Meta:
        model = Student
        fields = '__all__'

        widgets = {
            'dob': DateInput()
        }
    def save(self, commit=True):
        instance = super().save(commit=False)
        dob = self.cleaned_data.get('dob')

        if dob:
            today = date.today()
            instance.age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        else:
            instance.age = 0  # Ensure age is not None to prevent database errors

        if commit:
            instance.save()
        return instance


class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ['category', 'description', 'file']

        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),  # ✅ Correct
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
