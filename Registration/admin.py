from django.contrib import admin
from .models import Student, Year2025, Result


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "school_name", "division", "district", "upazila")
    search_fields = ("full_name", "user__username", "school_name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Year2025)
class Year2025Admin(admin.ModelAdmin):
    list_display = ("username", "year", "email", "school_name")
    list_filter = ("year",)
    search_fields = ("username", "email")


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "year", "selected_for_regional", "selected_for_national")
    list_filter = ("year",)
    search_fields = ("student__full_name", "student__user__username")
