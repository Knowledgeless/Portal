from django import forms
from django.contrib.auth.models import User
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

        email = cleaned.get("email")
        if email and User.objects.filter(email=email).exists():
            self.add_error("email", "This email is already registered.")

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
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exclude(student__id=self.instance.id).exists():
            raise forms.ValidationError("This email is already registered.")
        return email