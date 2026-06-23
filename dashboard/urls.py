from django.urls import path

from .views import (
    DashboardView,
    DashboardAnalyticsView
)

urlpatterns = [

    path(
        '',
        DashboardView.as_view(),
        name='dashboard'
    ),

    path(
        'analytics/',
        DashboardAnalyticsView.as_view(),
        name='dashboard-analytics'
    ),
]