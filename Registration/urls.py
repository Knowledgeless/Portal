# app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = "app"  # change to a nicer name if you want, e.g. "portal"

urlpatterns = [
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

    # Profile page (placeholder route — implement view later).
    # Several views above redirect to "profile" — implement it as you like.
    # path("profile/", views.profile_view, name="profile"),
]
