import csv
from io import BytesIO

from django.http import HttpResponse
from django.shortcuts import render
from openpyxl import Workbook
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from apps.accounts.decorators import staff_required
from apps.courses.models import Course, Registration
from apps.payments.models import Payment
from apps.students.models import Student


@staff_required
def reports_dashboard(request):
    semester = request.GET.get("semester", "")
    registrations = Registration.objects.select_related("student", "course")
    if semester:
        registrations = registrations.filter(semester=semester)
    context = {
        "semester": semester,
        "students_count": Student.objects.count(),
        "payments_total": sum(payment.amount for payment in Payment.objects.filter(status=Payment.Status.VERIFIED)),
        "registrations_count": registrations.count(),
        "course_counts": Course.objects.prefetch_related("registrations"),
    }
    return render(request, "admin_reports.html", context)


@staff_required
def registrations_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="registrations.csv"'
    writer = csv.writer(response)
    writer.writerow(["Reg Number", "Student", "Course", "Semester", "Registered At"])
    for registration in Registration.objects.select_related("student", "course"):
        writer.writerow([
            registration.student.reg_number,
            registration.student.full_name,
            registration.course.code,
            registration.semester,
            registration.registered_at,
        ])
    return response


@staff_required
def registrations_pdf(request):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 50
    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, y, "Registration Report")
    y -= 30
    pdf.setFont("Helvetica", 9)
    for registration in Registration.objects.select_related("student", "course")[:45]:
        pdf.drawString(50, y, f"{registration.student.reg_number} | {registration.course.code} | {registration.semester}")
        y -= 16
    pdf.save()
    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="registrations_report.pdf"'
    return response


@staff_required
def registrations_excel(request):
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Registrations"
    sheet.append(["Reg Number", "Student", "Course", "Semester", "Registered At"])
    for registration in Registration.objects.select_related("student", "course"):
        sheet.append([
            registration.student.reg_number,
            registration.student.full_name,
            registration.course.code,
            registration.semester,
            registration.registered_at.replace(tzinfo=None),
        ])
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)
    response = HttpResponse(
        buffer,
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    response["Content-Disposition"] = 'attachment; filename="registrations.xlsx"'
    return response

# Create your views here.
