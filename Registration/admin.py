# app/admin.py
from django.contrib import admin
from .models import Student, YearRegistration, Result

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "user", "school_name", "phone")
    search_fields = ("full_name", "school_name", "user__username", "user__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(YearRegistration)
class YearRegistrationAdmin(admin.ModelAdmin):
    list_display = ("username", "year", "school_name", "email", "student")
    search_fields = ("username", "school_name", "email")
    list_filter = ("year",)
    readonly_fields = ("created_at",)


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("student", "year", "selected_for_regional", "selected_for_national", "national_winner", "position")
    search_fields = ("student__full_name", "student__user__username")
    list_filter = ("year", "selected_for_regional", "selected_for_national", "national_winner")
