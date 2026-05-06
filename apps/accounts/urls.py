from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import RoleLoginView, audit_logs, dashboard, student_portal

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("portal/", student_portal, name="student_portal"),
    path("login/", RoleLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("audit-logs/", audit_logs, name="audit_logs"),
]
