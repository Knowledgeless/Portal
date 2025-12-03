from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import never_cache

from Registration.view_address import DIVISION_LIST, GEOGRAPHY_DATA

from .forms import NewUserRegistrationForm, ExistingUserUpdateForm, LoginForm
from .models import Student, Year2025, Result, active_year, generate_next_numeric_username, get_year_model

def home(request):
    return render(request, "home.html")



# ---------------- NEW REGISTRATION ----------------
def register_new(request):
    if request.user.is_authenticated:
        messages.info(request, "Logout First to Register a New Account.")
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
                            "3": "Primary", "4": "Primary", "5": "Primary",
                            "6": "Junior", "7": "Junior", "8": "Junior",
                            "9": "Secondary", "10": "Secondary",
                            "11": "Higher Secondary", "12": "Higher Secondary",
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
                    messages.error(request, f"Registration failed: {str(e)}")
                    return redirect("app:register_new")

            else:
                messages.error(request, "Form validation failed. Please check your inputs.")

        else:
            form = NewUserRegistrationForm()
            form.fields['division'].choices = [("", "-- Select Division --")] + [(d, d) for d in DIVISION_LIST]

        return render(request, "register.html", {"form": form})



# ---------------- PREVIOUS USER UPDATE ----------------
# @login_required
# def prev_user_update_registration(request):

#     student = get_object_or_404(Student, user=request.user)

#     if request.method == "POST":
#         form = ExistingUserUpdateForm(request.POST, instance=student)

#         if form.is_valid():
#             with transaction.atomic():

#                 # ---- 1. UPDATE USER TABLE ----
#                 request.user.email = form.cleaned_data["email"]
#                 request.user.save()

#                 # ---- 2. UPDATE CATEGORY BASED ON CLASS ----
#                 class_mapping = {
#                     "3": "Primary", "4": "Primary", "5": "Primary",
#                     "6": "Junior", "7": "Junior", "8": "Junior",
#                     "9": "Secondary", "10": "Secondary",
#                     "11": "Higher Secondary", "12": "Higher Secondary",
#                 }
#                 category = class_mapping.get(form.cleaned_data["student_class"], "Unknown")

#                 # ---- 3. UPDATE STUDENT TABLE ----
#                 student = form.save(commit=False)
#                 student.category_name = category
#                 student.save()

#                 # ---- 4. REGISTER / UPDATE YEAR-WISE TABLE ----
#                 year = active_year()
#                 YearModel = get_year_model(year)

#                 reg_obj, created = YearModel.objects.get_or_create(
#                     username=request.user.username,
#                     defaults={
#                         "email": request.user.email,
#                         "school_name": student.school_name,
#                         "student": student,
#                     }
#                 )

#                 if not created:
#                     reg_obj.email = request.user.email
#                     reg_obj.school_name = student.school_name
#                     reg_obj.student = student
#                     reg_obj.save()

#                 # ---- 5. RESULT TABLE ENTRY ----
#                 Result.objects.update_or_create(
#                     year=year,
#                     student=student,
#                     defaults={"registered_online": True}
#                 )

#             messages.success(request, "Your registration has been updated successfully.")
#             return redirect("profile")

#     else:
#         form = ExistingUserUpdateForm(instance=student)
#         form.fields["email"].initial = request.user.email

#     return render(request, "update_registration.html", {"form": form})


@never_cache
def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in.")
        return redirect('app:profile')

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        year = active_year()
        YearModel = get_year_model(year)
        already_registered = YearModel.objects.filter(student__user=user).exists()

        if already_registered:
            messages.success(request, f"You are already registered for {year+1}!")
            return redirect("app:profile")

        messages.info(request, f"Please update your information to register for {year + 1}.")
        return redirect("/profile/?show_update=1")

    return render(request, "login.html", {"form": form})

@never_cache
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)  # SAFE: using Django's logout()
        messages.warning(request, "You have been logged out.")
        return redirect("app:home")
    
    messages.info(request, "Login First")
    return redirect("app:login")
    return redirect("app:login")
@never_cache
def profile_view(request):
    # Ensure user is authenticated before accessing profile data
    if not request.user.is_authenticated:
        messages.info(request, "Login First")
        return redirect("app:login")
        messages.info(request, "Login First")
        return redirect("app:login")

    year = active_year() + 1
    student = get_object_or_404(Student, user=request.user)

    # Check if user is registered for current active year
    year0 = active_year()
    YearModel = get_year_model(year0)
    registered_for_year = YearModel.objects.filter(username=request.user.username).exists()

    # Show form if user explicitly requests it via ?register=1 or if user is registered (for edit)
    show_update = request.GET.get("show_update") or request.GET.get("register")
    form = None

    # Handle update POST from the profile page
    if request.method == "POST":
        form = ExistingUserUpdateForm(request.POST, instance=student)
        if form.is_valid():
            with transaction.atomic():
                # ---- 1. UPDATE USER TABLE ----
                request.user.email = form.cleaned_data.get("email", request.user.email)
                request.user.save()

                # ---- 2. UPDATE CATEGORY BASED ON CLASS ----
                class_mapping = {
                    "3": "Primary", "4": "Primary", "5": "Primary",
                    "6": "Junior", "7": "Junior", "8": "Junior",
                    "9": "Secondary", "10": "Secondary",
                    "11": "Higher Secondary", "12": "Higher Secondary",
                }
                category = class_mapping.get(form.cleaned_data.get("student_class"), "Unknown")

                # ---- 3. UPDATE STUDENT TABLE ----
                student = form.save(commit=False)
                student.category_name = category
                student.save()

                # ---- 4. REGISTER / UPDATE YEAR-WISE TABLE ----
                year0 = active_year()
                YearModel = get_year_model(year0)

                reg_obj, created = YearModel.objects.get_or_create(
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

                # ---- 5. RESULT TABLE ENTRY ----
                Result.objects.update_or_create(
                    year=year0,
                    student=student,
                    defaults={"registered_online": True}
                )

            messages.success(request, "Your registration has been updated successfully.")
            return redirect("app:profile")
        else:
            messages.error(request, "Form validation failed. Please check your inputs.")

    # If not a POST, prepare the form for display when requested
    elif show_update:
        form = ExistingUserUpdateForm(instance=student)
        form.fields["email"].initial = request.user.email
        # Populate dynamic choice fields
        form.fields['division'].choices = [("", "-- Select Division --")] + [(d, d) for d in DIVISION_LIST]
        if student.division in GEOGRAPHY_DATA:
            districts = list(GEOGRAPHY_DATA[student.division].keys())
            form.fields['district'].choices = [("", "-- Select District --")] + [(d, d) for d in districts]
        if student.division in GEOGRAPHY_DATA and student.district in GEOGRAPHY_DATA[student.division]:
            upazilas = GEOGRAPHY_DATA[student.division][student.district]
            form.fields['upazila'].choices = [("", "-- Select Upazila --")] + [(u, u) for u in upazilas]
    
    # Always initialize form if modal should be shown (for both register and edit)
    if (show_update or registered_for_year) and not form:
        form = ExistingUserUpdateForm(instance=student)
        form.fields["email"].initial = request.user.email
        # Populate dynamic choice fields
        form.fields['division'].choices = [("", "-- Select Division --")] + [(d, d) for d in DIVISION_LIST]
        if student.division in GEOGRAPHY_DATA:
            districts = list(GEOGRAPHY_DATA[student.division].keys())
            form.fields['district'].choices = [("", "-- Select District --")] + [(d, d) for d in districts]
        if student.division in GEOGRAPHY_DATA and student.district in GEOGRAPHY_DATA[student.division]:
            upazilas = GEOGRAPHY_DATA[student.division][student.district]
            form.fields['upazila'].choices = [("", "-- Select Upazila --")] + [(u, u) for u in upazilas]

    profile = Student.objects.select_related('user').get(user=request.user)
    return render(
        request, 
        "profile.html", 
        {
            "form": form, 
            "show_update": show_update,
            "show_modal": show_update or registered_for_year,  # Show modal HTML if registering or editing
            "year": year, 
            "profile_info": profile,
            "registered_for_year": registered_for_year
        }
    )
