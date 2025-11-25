# app/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import NewUserRegistrationForm, ExistingUserUpdateForm
from .models import Student, YearRegistration, get_year_model, generate_next_numeric_username, Result, active_year

# -------------- New registration (button: New Reg) --------------
def register_new(request):
    """
    For new users: create User -> Student -> YearRegistration -> Result.
    Username is auto-generated in the format: YY000001
    """
    if request.method == "POST":
        form = NewUserRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                # Auto-generate username (backend only, user never provides)
                username = generate_next_numeric_username()
                password = form.cleaned_data["password"]
                email = form.cleaned_data.get("email") or ""
                full_name = form.cleaned_data["full_name"]
                school_name = form.cleaned_data["school_name"]
                phone = form.cleaned_data.get("phone")
                address = form.cleaned_data.get("address")
                dob = form.cleaned_data.get("dob")

                # Create Django User
                user = User.objects.create_user(username=username, password=password, email=email)

                # Create Student profile
                student = Student.objects.create(
                    user=user,
                    full_name=full_name,
                    school_name=school_name,
                    phone=phone,
                    address=address,
                    dob=dob,
                )

                # Create year-wise registration record
                year = active_year()
                YearModel = get_year_model(year)
                if YearModel is YearRegistration:
                    YearModel.objects.create(
                        year=year,
                        username=username,
                        email=email,
                        school_name=school_name,
                        student=student
                    )
                else:
                    # per-year model
                    YearModel.objects.create(
                        year=year,
                        username=username,
                        email=email,
                        school_name=school_name,
                    )

                # Create initial Result record
                Result.objects.create(year=year, student=student, registered_online=True)

            messages.success(request, f"Registration successful. Your username: {username}")
            return redirect("login")
    else:
        form = NewUserRegistrationForm()

    return render(request, "register.html", {"form": form})


# -------------- Previous user flow (login required) --------------
@login_required
def prev_user_update_registration(request):
    """
    For previously registered users who log in:
    - Update Student profile and User.email
    - Ensure YearRegistration (or per-year model) exists for active year
    - Update year-wise record if it already exists
    - Ensure Result row exists for active year
    """
    student = get_object_or_404(Student, user=request.user)

    if request.method == "POST":
        form = ExistingUserUpdateForm(request.POST, instance=student)
        if form.is_valid():
            with transaction.atomic():
                # Update Student profile
                student = form.save()

                # Update User email
                email = form.cleaned_data.get("email")
                if email and email != request.user.email:
                    request.user.email = email
                    request.user.save(update_fields=["email"])

                # Get active year and YearModel
                year = active_year()
                YearModel = get_year_model(year)

                # --------------------------
                # Corrected part: update existing year-wise registration if exists
                # --------------------------
                reg_obj, created = YearModel.objects.get_or_create(
                    year=year,
                    username=request.user.username,
                    defaults={
                        "email": request.user.email,
                        "school_name": student.school_name,
                        "student": student if YearModel is YearRegistration else None,
                    },
                )
                if not created:
                    # Update existing record with latest info
                    reg_obj.email = request.user.email
                    reg_obj.school_name = student.school_name
                    if hasattr(reg_obj, "student"):
                        reg_obj.student = student
                    reg_obj.save()

                # --------------------------
                # Ensure a Result row exists for this student/year
                # --------------------------
                res_obj, _ = Result.objects.get_or_create(
                    year=year,
                    student=student,
                    defaults={"registered_online": True},
                )

            messages.success(request, "Your information has been updated for the current year.")
            return redirect("profile")
    else:
        initial = {"email": request.user.email}
        form = ExistingUserUpdateForm(instance=student, initial=initial)

    return render(request, "update_registration.html", {"form": form})



# -------------- Small helpers / API-like utilities --------------
def get_registration_for_year(username: str, year: int = None):
    """
    Return the registration record for a username in a year (or None).
    Works with either generic YearRegistration or per-year models.
    """
    year = year or active_year()
    YearModel = get_year_model(year)
    try:
        return YearModel.objects.get(username=username, year=year)
    except Exception:
        return None
    
