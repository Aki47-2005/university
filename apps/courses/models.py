from django.core.exceptions import ValidationError
from django.db import models


class Course(models.Model):
    class Weekday(models.TextChoices):
        MONDAY = "MON", "Monday"
        TUESDAY = "TUE", "Tuesday"
        WEDNESDAY = "WED", "Wednesday"
        THURSDAY = "THU", "Thursday"
        FRIDAY = "FRI", "Friday"
        SATURDAY = "SAT", "Saturday"

    code = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=160)
    credit_units = models.PositiveSmallIntegerField()
    department = models.CharField(max_length=120)
    prerequisites = models.ManyToManyField("self", symmetrical=False, blank=True)
    weekday = models.CharField(max_length=3, choices=Weekday.choices, default=Weekday.MONDAY)
    start_time = models.TimeField()
    end_time = models.TimeField()
    semester = models.CharField(max_length=30, default="Semester 1")
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["code"]

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("Course end time must be after start time.")

    def overlaps(self, other):
        return (
            self.weekday == other.weekday
            and self.start_time < other.end_time
            and other.start_time < self.end_time
        )

    def __str__(self):
        return f"{self.code} - {self.title}"


class Registration(models.Model):
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="registrations")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="registrations")
    semester = models.CharField(max_length=30)
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-registered_at"]
        constraints = [
            models.UniqueConstraint(fields=["student", "course", "semester"], name="unique_student_course_semester")
        ]

    def clean(self):
        if not self.student_id:
            return
        if not self.student.is_approved:
            raise ValidationError("Student must be approved before registration.")
        clearance = getattr(self.student, "clearance", None)
        if not clearance or not clearance.is_cleared:
            raise ValidationError("Financial clearance is required before registration.")
        existing = (
            Registration.objects.select_related("course")
            .filter(student=self.student, semester=self.semester)
            .exclude(pk=self.pk)
        )
        for registration in existing:
            if self.course.overlaps(registration.course):
                raise ValidationError(f"Timetable clash with {registration.course.code}.")

    def __str__(self):
        return f"{self.student.reg_number} - {self.course.code}"

# Create your models here.
