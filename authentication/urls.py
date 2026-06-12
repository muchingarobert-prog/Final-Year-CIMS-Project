from django.urls import path

from .views import (
    RegisterView,
    ProfileView,
    SearchUsersView,
    DashboardView,
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path(
        'register/',
        RegisterView.as_view()
    ),

    path(
        'login/',
        TokenObtainPairView.as_view()
    ),

    path(
        'token/refresh/',
        TokenRefreshView.as_view()
    ),

    path(
        'profile/',
        ProfileView.as_view()
    ),

    path(
        'search-users/',
        SearchUsersView.as_view()
    ),

    path(
        'dashboard/',
        DashboardView.as_view()
    ),
]