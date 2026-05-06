from datetime import time

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import User
from apps.courses.models import Course, Registration
from apps.payments.models import Clearance, Payment
from apps.results.models import Result
from apps.students.models import Student


class Command(BaseCommand):
    help = "Create sample users, students, courses, payments, registrations, and results."

    def handle(self, *args, **options):
        admin, _ = User.objects.get_or_create(username="admin", defaults={"role": User.Roles.ADMIN, "is_staff": True, "is_superuser": True})
        admin.set_password("Admin@12345")
        admin.save()

        staff, _ = User.objects.get_or_create(username="staff", defaults={"role": User.Roles.STAFF, "is_staff": True, "email": "staff@example.com"})
        staff.set_password("Staff@12345")
        staff.save()

        student_user, _ = User.objects.get_or_create(username="student", defaults={"role": User.Roles.STUDENT, "email": "student@example.com"})
        student_user.set_password("Student@12345")
        student_user.save()

        student, _ = Student.objects.get_or_create(
            user=student_user,
            defaults={
                "full_name": "Amina Nsubuga",
                "reg_number": "2026/U/001",
                "programme": "Bachelor of Information Systems",
                "year_of_study": 2,
                "is_approved": True,
            },
        )

        course1, _ = Course.objects.get_or_create(
            code="ICT2101",
            defaults={
                "title": "Database Systems",
                "credit_units": 4,
                "department": "Computing",
                "weekday": Course.Weekday.MONDAY,
                "start_time": time(9, 0),
                "end_time": time(11, 0),
                "semester": "Semester 1",
            },
        )
        course2, _ = Course.objects.get_or_create(
            code="ICT2204",
            defaults={
                "title": "Web Application Development",
                "credit_units": 3,
                "department": "Computing",
                "weekday": Course.Weekday.TUESDAY,
                "start_time": time(10, 0),
                "end_time": time(12, 0),
                "semester": "Semester 1",
            },
        )

        Payment.objects.get_or_create(
            student=student,
            reference="PAY-2026-001",
            defaults={
                "amount": 1500000,
                "status": Payment.Status.VERIFIED,
                "verified_by": admin,
                "verified_at": timezone.now(),
            },
        )
        Clearance.objects.update_or_create(
            student=student,
            defaults={"is_cleared": True, "cleared_by": admin, "cleared_at": timezone.now(), "notes": "Sample clearance"},
        )

        Registration.objects.get_or_create(student=student, course=course1, semester="Semester 1")
        Registration.objects.get_or_create(student=student, course=course2, semester="Semester 1")
        Result.objects.get_or_create(student=student, course=course1, semester="Semester 1", defaults={"grade": "A"})
        Result.objects.get_or_create(student=student, course=course2, semester="Semester 1", defaults={"grade": "B+"})

        self.stdout.write(self.style.SUCCESS("Sample data created. Logins: admin/Admin@12345, staff/Staff@12345, student/Student@12345"))
