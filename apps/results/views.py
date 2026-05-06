from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import staff_required
from apps.accounts.models import AuditLog
from apps.notifications.utils import notify

from .forms import ResultForm
from .models import Result


def result_list(request):
    if request.user.is_student_role and not request.user.is_staff:
        student = getattr(request.user, "student_profile", None)
        results = Result.objects.filter(student=student).select_related("course") if student else Result.objects.none()
    else:
        results = Result.objects.select_related("student", "course")
    total_units = sum(result.course.credit_units for result in results)
    total_points = sum(result.weighted_points for result in results)
    gpa = round(total_points / total_units, 2) if total_units else None
    page = Paginator(results, 15).get_page(request.GET.get("page"))
    return render(request, "results.html", {"page": page, "gpa": gpa})


@staff_required
def result_create(request):
    form = ResultForm(request.POST or None)
    if form.is_valid():
        result = form.save()
        AuditLog.objects.create(user=request.user, action=f"Uploaded result for {result.student.reg_number}", ip_address=request.client_ip)
        notify(result.student.user, "Result uploaded", f"{result.course.code} result is now available.", "INFO")
        messages.success(request, "Result saved.")
        return redirect("result_list")
    return render(request, "form.html", {"form": form, "title": "Upload Result"})


@staff_required
def result_update(request, pk):
    result = get_object_or_404(Result, pk=pk)
    form = ResultForm(request.POST or None, instance=result)
    if form.is_valid():
        result = form.save()
        AuditLog.objects.create(user=request.user, action=f"Updated result for {result.student.reg_number}", ip_address=request.client_ip)
        messages.success(request, "Result updated.")
        return redirect("result_list")
    return render(request, "form.html", {"form": form, "title": "Edit Result"})


@staff_required
def result_delete(request, pk):
    result = get_object_or_404(Result, pk=pk)
    if request.method == "POST":
        AuditLog.objects.create(user=request.user, action=f"Deleted result for {result.student.reg_number}", ip_address=request.client_ip)
        result.delete()
        messages.success(request, "Result deleted.")
        return redirect("result_list")
    return render(request, "confirm_delete.html", {"object": result, "title": "Delete Result"})

# Create your views here.
