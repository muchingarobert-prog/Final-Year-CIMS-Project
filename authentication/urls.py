from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    RegisterView,
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
        TokenObtainPairView.as_view()
    ),

    path(
        "logout/",
        LogoutView.as_view()
    ),

    path(
        "token/refresh/",
        TokenRefreshView.as_view()
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