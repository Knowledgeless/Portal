# app/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Student

class NewUserRegistrationForm(forms.Form):
    """
    Minimal fields to register a new participant.
    If username left blank, system auto-generates a numeric username.
    """
    username = forms.CharField(max_length=50, required=False,
                               help_text="Leave blank to auto-generate numeric username.")
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    email = forms.EmailField(required=False)
    full_name = forms.CharField(max_length=200)
    school_name = forms.CharField(max_length=200)
    phone = forms.CharField(max_length=20, required=False)
    address = forms.CharField(max_length=300, required=False)
    dob = forms.DateField(required=False)

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if username:
            if User.objects.filter(username=username).exists():
                raise forms.ValidationError("Username already taken.")
            # optional: enforce numeric pattern if you want
        return username


class ExistingUserUpdateForm(forms.ModelForm):
    """
    Allow existing logged-in users to update their profile for current and future years.
    Username is intentionally excluded.
    Email is separate field (User.email).
    """
    email = forms.EmailField(required=False)

    class Meta:
        model = Student
        fields = ["full_name", "school_name", "phone", "address", "dob"]
