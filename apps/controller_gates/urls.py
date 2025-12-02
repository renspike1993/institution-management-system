from django.urls import path
from . import views

urlpatterns = [
    path("attendance/", views.attendance_logs, name="turnstile_attendance"),
]
