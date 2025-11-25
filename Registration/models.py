# app/models.py
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils import timezone
from django.apps import apps

# ---- Student profile ----
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile")
    full_name = models.CharField(max_length=200)
    school_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.user.username})"


# ---- Generic year-wise registration (recommended single-table approach) ----
class YearRegistration(models.Model):
    year = models.PositiveIntegerField(db_index=True)
    username = models.CharField(max_length=50, db_index=True)  # store numeric username like 25000001
    email = models.EmailField(blank=True, null=True)
    school_name = models.CharField(max_length=200, blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("year", "username")
        ordering = ["-year", "username"]

    def __str__(self):
        return f"{self.username} - {self.year}"


# ---- Results table ----
class Result(models.Model):
    year = models.PositiveIntegerField(db_index=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="results")
    registered_online = models.BooleanField(default=False)
    participated_online = models.BooleanField(default=False)
    selected_for_regional = models.BooleanField(default=False)
    selected_for_national = models.BooleanField(default=False)
    participated_national = models.BooleanField(default=False)
    national_winner = models.BooleanField(default=False)
    position = models.PositiveIntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("year", "student")

    def __str__(self):
        return f"Result {self.student} - {self.year}"


# ---- Helpers ----
def get_year_model(year: int):
    """
    If you later add a per-year model named Year{year} (eg Year2026),
    this will return that model. Otherwise returns YearRegistration.
    """
    model_name = f"Year{year}"
    try:
        # assume same app label as this models.py file
        app_label = __name__.split(".")[0]
        return apps.get_model(app_label=app_label, model_name=model_name)
    except (LookupError, ValueError):
        return YearRegistration


def generate_next_numeric_username():
    """
    Auto-generate a unique username like YY000001.
    - YY: last 2 digits of current year
    - 00000: fixed
    - increment: start from 1 or max+1
    """
    year_suffix = str(timezone.now().year)[-2:]  # e.g., 2025 -> '25'
    prefix = f"{year_suffix}00000"

    # Get the last numeric username starting with this prefix
    last_user = (
        User.objects.filter(username__startswith=prefix)
        .order_by("-username")
        .first()
    )

    if last_user:
        try:
            last_number = int(last_user.username)
            next_number = last_number + 1
        except ValueError:
            # fallback if something weird is in the DB
            next_number = int(prefix) + 1
    else:
        next_number = int(prefix) + 1

    return str(next_number)


def active_year():
    """
    Return active year. Use settings.ACTIVE_YEAR if set; otherwise current year.
    """
    return getattr(settings, "ACTIVE_YEAR", timezone.now().year)
