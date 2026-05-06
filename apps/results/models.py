from django.db import models


class Result(models.Model):
    GRADE_POINTS = {
        "A": 5.0,
        "B+": 4.5,
        "B": 4.0,
        "C+": 3.5,
        "C": 3.0,
        "D": 2.0,
        "F": 0.0,
    }

    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="results")
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE, related_name="results")
    grade = models.CharField(max_length=2)
    semester = models.CharField(max_length=30)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["student__reg_number", "semester", "course__code"]
        constraints = [
            models.UniqueConstraint(fields=["student", "course", "semester"], name="unique_student_result_semester")
        ]

    @property
    def grade_point(self):
        return self.GRADE_POINTS.get(self.grade.upper(), 0.0)

    @property
    def weighted_points(self):
        return self.grade_point * self.course.credit_units

    def __str__(self):
        return f"{self.student.reg_number} - {self.course.code}: {self.grade}"

# Create your models here.
