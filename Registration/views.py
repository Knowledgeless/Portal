from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404

from .forms import NewUserRegistrationForm, ExistingUserUpdateForm
from .models import Student, YearRegistration, Result, active_year, generate_next_numeric_username, get_year_model

def home(request):
    return render(request, "home.html")



# ---------------- NEW REGISTRATION ----------------
def register_new(request):
    if request.method == "POST":
        form = NewUserRegistrationForm(request.POST)
        if form.is_valid():
            with transaction.atomic():

                username = generate_next_numeric_username()
                password = form.cleaned_data["password"]

                # User
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    email=form.cleaned_data["email"]
                )
                user.save()
                # Category selection
                class_mapping = {
                    "3": "Primary",
                    "4": "Primary",
                    "5": "Primary",
                    "6": "Junior",
                    "7": "Junior",
                    "8": "Junior",
                    "9": "Secondary",
                    "10": "Secondary",
                    "11": "Higher Secondary",
                    "12": "Higher Secondary",
                }

                category = class_mapping[form.cleaned_data["student_class"]]

                # Student
                student = Student.objects.create(
                    user=user,
                    full_name=form.cleaned_data["full_name"],
                    school_name=form.cleaned_data["school_name"],
                    phone=form.cleaned_data["phone"],
                    division=form.cleaned_data["division"],
                    district=form.cleaned_data["district"],
                    upazila=form.cleaned_data["upazila"],
                    gender=form.cleaned_data["gender"],
                    student_class=form.cleaned_data["student_class"],
                    category_name=category,
                    dob=form.cleaned_data["dob"]
                )
                student.save()
                # Year-wise entry
                year = active_year()
                YearModel = get_year_model(year)

                YearModel.objects.create(
                    year=year,
                    username=username,
                    email=user.email,
                    school_name=student.school_name,
                    student=student,
                )
                YearModel.save()
                # Result row
                Result.objects.create(
                    year=year,
                    student=student,
                    registered_online=True
                )

                messages.success(request, f"Registration Successful! Your username is {username}")
                return redirect("login")
                print("User registered successfully.")
            messages.error(request, "An error occurred during registration. Please try again.")
            return redirect("register_new")
            print(form.errors)
    else:
        form = NewUserRegistrationForm()
    messages.error(request, "Something went wrong. Please try again.")
    return render(request, "register.html", {"form": form})


# ---------------- PREVIOUS USER UPDATE ----------------
@login_required
def prev_user_update_registration(request):

    student = get_object_or_404(Student, user=request.user)

    if request.method == "POST":
        form = ExistingUserUpdateForm(request.POST, instance=student)
        if form.is_valid():
            with transaction.atomic():

                student = form.save()
                request.user.email = form.cleaned_data["email"]
                request.user.save()

                year = active_year()
                YearModel = get_year_model(year)

                reg_obj, created = YearModel.objects.get_or_create(
                    year=year,
                    username=request.user.username,
                    defaults={
                        "email": request.user.email,
                        "school_name": student.school_name,
                        "student": student,
                    }
                )

                if not created:
                    reg_obj.email = request.user.email
                    reg_obj.school_name = student.school_name
                    reg_obj.student = student
                    reg_obj.save()

                Result.objects.get_or_create(
                    year=year,
                    student=student,
                    defaults={"registered_online": True}
                )

            messages.success(request, "Your profile has been updated for this year.")
            return redirect("profile")

    else:
        form = ExistingUserUpdateForm(instance=student, initial={"email": request.user.email})

    return render(request, "update_registration.html", {"form": form})
