import qrcode
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

from apps.accounts.decorators import staff_required
from apps.accounts.models import AuditLog
from apps.notifications.utils import notify

from .forms import CourseForm, RegistrationForm
from .models import Course, Registration


@staff_required
def course_list(request):
    query = request.GET.get("q", "")
    courses = Course.objects.prefetch_related("prerequisites")
    if query:
        courses = courses.filter(code__icontains=query) | courses.filter(title__icontains=query)
    page = Paginator(courses.distinct(), 10).get_page(request.GET.get("page"))
    return render(request, "courses/course_list.html", {"page": page, "query": query})


@staff_required
def course_create(request):
    form = CourseForm(request.POST or None)
    if form.is_valid():
        course = form.save()
        AuditLog.objects.create(user=request.user, action=f"Created course {course.code}", ip_address=request.client_ip)
        messages.success(request, "Course created successfully.")
        return redirect("course_list")
    return render(request, "form.html", {"form": form, "title": "Add Course"})


@staff_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)
    form = CourseForm(request.POST or None, instance=course)
    if form.is_valid():
        course = form.save()
        AuditLog.objects.create(user=request.user, action=f"Updated course {course.code}", ip_address=request.client_ip)
        messages.success(request, "Course updated successfully.")
        return redirect("course_list")
    return render(request, "form.html", {"form": form, "title": "Edit Course"})


@staff_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        AuditLog.objects.create(user=request.user, action=f"Deleted course {course.code}", ip_address=request.client_ip)
        course.delete()
        messages.success(request, "Course deleted.")
        return redirect("course_list")
    return render(request, "confirm_delete.html", {"object": course, "title": "Delete Course"})


def register_course(request):
    student = getattr(request.user, "student_profile", None)
    if not student:
        messages.error(request, "No student profile is linked to this account.")
        return redirect("student_portal")
    form = RegistrationForm(request.POST or None, student=student)
    registrations = Registration.objects.filter(student=student).select_related("course")
    if request.method == "POST" and form.is_valid():
        registration = form.save(commit=False)
        registration.student = student
        registration.save()
        AuditLog.objects.create(
            user=request.user,
            action=f"Registered {student.reg_number} for {registration.course.code}",
            ip_address=getattr(request, "client_ip", None),
        )
        notify(request.user, "Course registration complete", f"You registered {registration.course.code}.", "SUCCESS")
        messages.success(request, "Course registered successfully.")
        return redirect("register_course")
    return render(request, "register_course.html", {"form": form, "registrations": registrations})


def registration_slip(request):
    student = getattr(request.user, "student_profile", None)
    if not student:
        messages.error(request, "No student profile is linked to this account.")
        return redirect("student_portal")
    registrations = Registration.objects.filter(student=student).select_related("course")
    verification_text = f"{student.reg_number}|{registrations.count()}|university-registration"
    qr_image = qrcode.make(verification_text)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{student.reg_number}_registration_slip.pdf"'
    pdf = canvas.Canvas(response, pagesize=A4)
    width, height = A4
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(1 * inch, height - 1 * inch, "University Registration Slip")
    pdf.setFont("Helvetica", 11)
    pdf.drawString(1 * inch, height - 1.35 * inch, f"Student: {student.full_name}")
    pdf.drawString(1 * inch, height - 1.6 * inch, f"Registration Number: {student.reg_number}")
    pdf.drawString(1 * inch, height - 1.85 * inch, f"Programme: {student.programme}")
    y = height - 2.4 * inch
    pdf.setFont("Helvetica-Bold", 11)
    pdf.drawString(1 * inch, y, "Registered Courses")
    y -= 0.3 * inch
    pdf.setFont("Helvetica", 10)
    for registration in registrations:
        pdf.drawString(1 * inch, y, f"{registration.course.code} - {registration.course.title} ({registration.semester})")
        y -= 0.25 * inch
    pdf.drawInlineImage(qr_image, width - 2.2 * inch, height - 2.3 * inch, 1.2 * inch, 1.2 * inch)
    pdf.showPage()
    pdf.save()
    return response

# Create your views here.
