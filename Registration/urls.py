# app/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views, view_address

app_name = "app"  # change to a nicer name if you want, e.g. "portal"

urlpatterns = [
    path("", views.home, name="home"),
    path("home", views.home, name="home"),
    path("register/", views.register_new, name="register_new"),
    path("manage/", views.admin_view, name="admin_view"),
    # Admin: view any user's profile by username (placed BEFORE profile/ to take precedence)
    path("profile/<str:username>/", views.admin_profile_view, name="admin_profile"),
    path("manage/search/", views.admin_search_view, name="admin_search"),
    # path("update-existing-user/", views.prev_user_update_registration, name="prev_user_update_registration"),
    # Previous user flow (login required)  
    # path("update-registration/", views.prev_user_update_registration, name="prev_user_update_registration"),

    # Login / Logout using Django auth views
    path("login/",views.login_view,name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.profile_view, name="profile"),
    # path("profile/update-ajax/", views.update_profile_ajax, name="update_profile_ajax"),

    path("api/divisions/", view_address.api_divisions, name="api_divisions"),
    path("api/districts/", view_address.api_districts, name="api_districts"),
    path("api/upazilas/", view_address.api_upazilas, name="api_upazilas"),
]
