from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from apps.accounts.decorators import staff_required
from apps.accounts.models import AuditLog
from apps.payments.models import Clearance

from .forms import StudentForm
from .models import Student


@staff_required
def student_list(request):
    query = request.GET.get("q", "")
    students = Student.objects.select_related("user")
    if query:
        students = students.filter(full_name__icontains=query) | students.filter(reg_number__icontains=query)
    page = Paginator(students.distinct(), 10).get_page(request.GET.get("page"))
    return render(request, "students/student_list.html", {"page": page, "query": query})


@staff_required
def student_create(request):
    form = StudentForm(request.POST or None)
    if form.is_valid():
        student = form.save()
        Clearance.objects.get_or_create(student=student)
        AuditLog.objects.create(user=request.user, action=f"Created student {student.reg_number}", ip_address=request.client_ip)
        messages.success(request, "Student created successfully.")
        return redirect("student_list")
    return render(request, "form.html", {"form": form, "title": "Add Student"})


@staff_required
def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, instance=student)
    if form.is_valid():
        student = form.save()
        Clearance.objects.get_or_create(student=student)
        AuditLog.objects.create(user=request.user, action=f"Updated student {student.reg_number}", ip_address=request.client_ip)
        messages.success(request, "Student updated successfully.")
        return redirect("student_list")
    return render(request, "form.html", {"form": form, "title": "Edit Student"})


@staff_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        AuditLog.objects.create(user=request.user, action=f"Deleted student {student.reg_number}", ip_address=request.client_ip)
        student.delete()
        messages.success(request, "Student deleted.")
        return redirect("student_list")
    return render(request, "confirm_delete.html", {"object": student, "title": "Delete Student"})

# Create your views here.
