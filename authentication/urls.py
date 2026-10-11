from django.urls import path

from .views import (
    RegisterView,
    LoginView,
    RefreshTokenView,
    ProfileView,
    DashboardView,
    LogoutView,
    SearchUsersView,
    PasswordResetRequestView,
    PasswordResetConfirmView,
)

urlpatterns = [

    path(
        "register/",
        RegisterView.as_view()
    ),

    path(
        "login/",
        LoginView.as_view()
    ),

    path(
        "logout/",
        LogoutView.as_view()
    ),

    path(
        "token/refresh/",
        RefreshTokenView.as_view()
    ),

    path(
        "profile/",
        ProfileView.as_view()
    ),

    path(
        "dashboard/",
        DashboardView.as_view()
    ),

    path(
        "search-users/",
        SearchUsersView.as_view()
    ),

    path(
        "password-reset/",
        PasswordResetRequestView.as_view()
    ),

    path(
        "password-reset-confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view()
    ),
]