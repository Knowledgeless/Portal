from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm

from Registration.view_address import DIVISION_LIST, GEOGRAPHY_DATA

from .forms import NewUserRegistrationForm, ExistingUserUpdateForm, LoginForm
from .models import Student, Year2025, Result, active_year, generate_next_numeric_username, get_year_model

def home(request):
    return render(request, "home.html")



# ---------------- NEW REGISTRATION ----------------
def register_new(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect("app:profile")
    else:
        if request.method == "POST":
            # Dynamically populate choices for validation
            form = NewUserRegistrationForm(request.POST)
            form.fields['division'].choices = [("", "-- Select Division --")] + [(d, d) for d in DIVISION_LIST]

            # Populate districts based on submitted division
            submitted_division = request.POST.get("division")
            if submitted_division in GEOGRAPHY_DATA:
                districts = list(GEOGRAPHY_DATA[submitted_division].keys())
            else:
                districts = []
            form.fields['district'].choices = [("", "-- Select District --")] + [(d, d) for d in districts]

            # Populate upazilas based on submitted division & district
            submitted_district = request.POST.get("district")
            if submitted_division in GEOGRAPHY_DATA and submitted_district in GEOGRAPHY_DATA[submitted_division]:
                upazilas = GEOGRAPHY_DATA[submitted_division][submitted_district]
            else:
                upazilas = []
            form.fields['upazila'].choices = [("", "-- Select Upazila --")] + [(u, u) for u in upazilas]

            if form.is_valid():
                # Grab values
                division = form.cleaned_data.get("division")
                district = form.cleaned_data.get("district")
                upazila = form.cleaned_data.get("upazila")

                print("Division:", division, "District:", district, "Upazila:", upazila)

                try:
                    with transaction.atomic():
                        username = generate_next_numeric_username()
                        password = form.cleaned_data["password"]

                        while User.objects.filter(username=username).exists():
                            username = str(int(username) + 1)
                        # Create Django User
                        user = User.objects.create_user(
                                    username=username,
                                    password=password,
                                    email=form.cleaned_data["email"]
                                )
                        

                        # Category mapping
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
                        category = class_mapping.get(form.cleaned_data["student_class"], "Unknown")

                        # Create Student
                        student = Student.objects.create(
                            user=user,
                            full_name=form.cleaned_data["full_name"],
                            school_name=form.cleaned_data["school_name"],
                            phone=form.cleaned_data["phone"],
                            division=division,
                            district=district,
                            upazila=upazila,
                            gender=form.cleaned_data["gender"],
                            student_class=form.cleaned_data["student_class"],
                            category_name=category,
                            dob=form.cleaned_data["dob"]
                        )

                        # Year-wise entry
                        year = active_year()
                        YearModel = get_year_model(year)
                        YearModel.objects.create(
                            # year=year,
                            username=username,
                            email=user.email,
                            school_name=student.school_name,
                            student=student,
                        )

                        # Result entry
                        Result.objects.create(
                            year=year,
                            student=student,
                            registered_online=True
                        )

                        messages.success(request, f"Registration Successful! Your username is {username}")
                        return redirect("/login")

                except Exception as e:
                    print("Error during registration:", str(e))
                    messages.error(request, f"Registration failed: {str(e)}")
                    return redirect("app:register_new")

            else:
                print("Form errors:", form.errors)
                messages.error(request, "Form validation failed. Please check your inputs.")

        else:
            form = NewUserRegistrationForm()
            form.fields['division'].choices = [("", "-- Select Division --")] + [(d, d) for d in DIVISION_LIST]

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


def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, "You are already logged in.")
        return redirect('app:profile')

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        print(form)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("app:profile")

        messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm(request)

    return render(request, "login.html", {"form": form})

@login_required
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)  # SAFE: using Django's logout()
        messages.warning(request, "Logged out successfully.")
        return redirect("app:login")
    else:
        messages.info("Login First")
        return redirect("app:login")

@login_required
def profile_view(request):
    return render(request, "profile.html")