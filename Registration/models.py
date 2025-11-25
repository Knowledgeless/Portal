from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.apps import apps


# ---------------- Student Profile ----------------
class Student(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="student_profile"
    )

    # ----- Basic Info -----
    full_name = models.CharField(max_length=200, default="Unknown")
    school_name = models.CharField(max_length=200, default="Not Provided")
    phone = models.CharField(max_length=20, default="N/A")

    # ----- Address Fields -----
    division = models.CharField(max_length=100, default="Not Selected")
    district = models.CharField(max_length=100, default="Not Selected")
    upazila = models.CharField(max_length=100, default="Not Selected")

    # ----- Extra -----
    gender = models.CharField(max_length=20, default="Not Specified")
    student_class = models.CharField(max_length=20, default="Unknown")
    category_name = models.CharField(max_length=50, default="Unknown")

    dob = models.DateField(default=timezone.now)  # Prevent migration error

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"


# ---------------- Year-wise Registration ----------------
class YearRegistration(models.Model):
    year = models.PositiveIntegerField(db_index=True, default=timezone.now().year)
    username = models.CharField(max_length=50, db_index=True, default="00000000")
    email = models.EmailField(default="not_provided@example.com")
    school_name = models.CharField(max_length=200, default="Not Provided")

    student = models.ForeignKey(
        Student,
        on_delete=models.SET_NULL,
        null=True,
        default=None
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("year", "username")
        ordering = ["-year", "username"]

    def __str__(self):
        return f"{self.username} - {self.year}"


# ---------------- Result Table ----------------
class Result(models.Model):
    year = models.PositiveIntegerField(db_index=True, default=timezone.now().year)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="results"
    )

    registered_online = models.BooleanField(default=False)
    participated_online = models.BooleanField(default=False)
    selected_for_regional = models.BooleanField(default=False)
    selected_for_national = models.BooleanField(default=False)
    participated_national = models.BooleanField(default=False)
    national_winner = models.BooleanField(default=False)

    position = models.PositiveIntegerField(null=True, blank=True, default=None)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("year", "student")

    def __str__(self):
        return f"{self.student} - {self.year}"


# ---------------- Helpers ----------------
def get_year_model(year: int):
    model_name = f"Year{year}"
    try:
        app_label = __name__.split(".")[0]
        return apps.get_model(app_label, model_name)
    except Exception:
        return YearRegistration


def generate_next_numeric_username():
    year_suffix = str(timezone.now().year)[-2:]
    prefix = f"{year_suffix}00000"

    last_user = User.objects.filter(username__startswith=prefix).order_by("-username").first()

    if last_user:
        return str(int(last_user.username) + 1)
    else:
        return str(int(prefix) + 1)


def active_year():
    return getattr(settings, "ACTIVE_YEAR", timezone.now().year)


def get_category(student_class: str):
    class_to_category = {
        "Class 3": "Primary",
        "Class 4": "Primary",
        "Class 5": "Primary",
        "Class 6": "Junior",
        "Class 7": "Junior",
        "Class 8": "Junior",
        "Class 9": "Senior",
        "Class 10": "Senior",
        "Class 11": "Higher Secondary",
        "Class 12": "Higher Secondary",
    }
    return class_to_category.get(student_class, "Unknown")
