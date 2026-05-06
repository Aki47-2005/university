from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from apps.accounts.decorators import staff_required
from apps.accounts.models import AuditLog, User
from apps.courses.models import Registration
from apps.payments.models import Payment
from apps.students.models import Student


class RoleLoginView(LoginView):
    template_name = "login.html"

    def get_success_url(self):
        user = self.request.user
        if user.is_admin_role or user.is_staff_role:
            return "/"
        return "/portal/"


@login_required
def dashboard(request):
    if request.user.is_student_role and not request.user.is_staff:
        return redirect("student_portal")
    context = {
        "total_students": Student.objects.count(),
        "total_users": User.objects.count(),
        "total_registrations": Registration.objects.count(),
        "total_payments": Payment.objects.count(),
        "recent_logs": AuditLog.objects.select_related("user")[:8],
        "recent_payments": Payment.objects.select_related("student")[:5],
    }
    return render(request, "dashboard.html", context)


@login_required
def student_portal(request):
    student = getattr(request.user, "student_profile", None)
    registrations = []
    results = []
    gpa = None
    if student:
        registrations = student.registrations.select_related("course")[:10]
        results = student.results.select_related("course")
        total_units = sum(result.course.credit_units for result in results)
        total_points = sum(result.weighted_points for result in results)
        gpa = round(total_points / total_units, 2) if total_units else None
    return render(
        request,
        "student_portal.html",
        {"student": student, "registrations": registrations, "results": results, "gpa": gpa},
    )


@staff_required
def audit_logs(request):
    logs = AuditLog.objects.select_related("user")
    return render(request, "audit_logs.html", {"logs": logs})

# Create your views here.
