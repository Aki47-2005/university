from django.urls import path

from . import views

urlpatterns = [
    path("", views.reports_dashboard, name="reports_dashboard"),
    path("registrations.csv", views.registrations_csv, name="registrations_csv"),
    path("registrations.pdf", views.registrations_pdf, name="registrations_pdf"),
    path("registrations.xlsx", views.registrations_excel, name="registrations_excel"),
]
