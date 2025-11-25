# app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, view_address

app_name = "app"  # change to a nicer name if you want, e.g. "portal"

urlpatterns = [
    path("", views.home, name="home"),
    # New registration (button: New Reg)
    path("register/", views.register_new, name="register_new"),

    # Previous user flow (login required)
    path("update-registration/", views.prev_user_update_registration, name="prev_user_update_registration"),

    # Login / Logout using Django auth views
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="app:login"),
        name="logout",
    ),
    path("api/divisions/", view_address.api_divisions, name="api_divisions"),
    path("api/districts/", view_address.api_districts, name="api_districts"),
    path("api/upazilas/", view_address.api_upazilas, name="api_upazilas"),
    # Profile page (placeholder route — implement view later).
    # Several views above redirect to "profile" — implement it as you like.
    # path("profile/", views.profile_view, name="profile"),
]
