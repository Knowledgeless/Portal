from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Student

class NewUserRegistrationForm(forms.Form):
    # ---------- Basic Info ----------
    full_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Full Name",
            "required": True
        })
    )
    school_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "School Name",
            "required": True
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Email Address",
            "required": True
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Mobile (01xxxxxxxxx)",
            "required": True
        })
    )

    # ---------- Password ----------
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Password",
            "required": True,
            "minlength": "8"
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Confirm Password",
            "required": True
        })
    )

    # ---------- Academic ----------
    student_class = forms.ChoiceField(
        choices=[("", "--- Select Class ---")] + [(str(i), f"Class {i}") for i in range(3, 13)],
        widget=forms.Select(attrs={"class": "form-select", "required": True})
    )
    gender = forms.ChoiceField(
        choices=[("", "--- Select Gender ---"), ("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
        widget=forms.Select(attrs={"class": "form-select", "required": True})
    )
    dob = forms.DateField(
        widget=forms.DateInput(attrs={
            "type": "date",
            "class": "form-control",
            "required": True
        })
    )

    # ---------- Address ----------
    division = forms.ChoiceField(
        choices=[("", "-- Select Division --")],
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "id_division",
            "required": True
        })
    )
    district = forms.ChoiceField(
        choices=[("", "-- Select District --")],
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "id_district",
            "required": True
        })
    )
    upazila = forms.ChoiceField(
        choices=[("", "-- Select Upazila --")],
        widget=forms.Select(attrs={
            "class": "form-select",
            "id": "id_upazila",
            "required": True
        })
    )


    # ---------- Clean Methods ----------
    def clean(self):
        cleaned = super().clean()

        password = cleaned.get("password")
        confirm_password = cleaned.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        
        return cleaned


class ExistingUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "required": True})
    )

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
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "school_name": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "phone": forms.TextInput(attrs={"class": "form-control", "required": True}),
            "division": forms.Select(attrs={"class": "form-select", "required": True}),
            "district": forms.Select(attrs={"class": "form-select", "required": True}),
            "upazila": forms.Select(attrs={"class": "form-select", "required": True}),
            "gender": forms.Select(attrs={"class": "form-select", "required": True}),
            "student_class": forms.Select(attrs={"class": "form-select", "required": True}),
            "dob": forms.DateInput(attrs={"type": "date", "class": "form-control", "required": True}),
        }
    def clean_email(self):
        return self.cleaned_data.get("email")
    
class LoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control w-100',
            'placeholder': 'Username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control w-100',
            'placeholder': 'Password',
        })


