from django import forms
from django.contrib.auth.models import User
from .models import Student


class NewUserRegistrationForm(forms.Form):

    # Basic Info
    full_name = forms.CharField(max_length=200)
    school_name = forms.CharField(max_length=200)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)

    # Password
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    # Academic
    student_class = forms.ChoiceField(choices=[
        ("3", "Class 3"),
        ("4", "Class 4"),
        ("5", "Class 5"),
        ("6", "Class 6"),
        ("7", "Class 7"),
        ("8", "Class 8"),
        ("9", "Class 9"),
        ("10", "Class 10"),
        ("11", "Class 11"),
        ("12", "Class 12"),
    ])

    gender = forms.ChoiceField(choices=[
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    ])

    dob = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    # Address
    division = forms.CharField()
    district = forms.CharField()
    upazila = forms.CharField()

    # Confirmation
    accept_terms = forms.BooleanField()

    # Auto category assignment
    def clean(self):
        cleaned = super().clean()

        if cleaned.get("password") != cleaned.get("confirm_password"):
            raise forms.ValidationError("Passwords do not match.")

        return cleaned


class ExistingUserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Student
        fields = [
            "full_name",
            "school_name",
            "phone",
            "division",
            "district",
            "upazila",
            "gender",
            "student_class",
            "dob",
        ]
