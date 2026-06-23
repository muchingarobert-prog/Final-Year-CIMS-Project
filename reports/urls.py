from django.urls import path

from .views import (
    ReportsView,
    AttendanceReportView,
    CommitteeReportView,
    EventReportView,
    MemberReportView,
    FinanceReportView,
)

urlpatterns = [

    path(
        '',
        ReportsView.as_view()
    ),

    path(
        'attendance/',
        AttendanceReportView.as_view()
    ),

    path(
        'committees/',
        CommitteeReportView.as_view()
    ),

    path(
        'events/',
        EventReportView.as_view()
    ),

    path(
        'members/',
        MemberReportView.as_view()
    ),

    path(
        'finances/',
        FinanceReportView.as_view()
    ),
]