from django.conf import settings
from django.db import models
from django.utils import timezone


class Payment(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending"
        VERIFIED = "VERIFIED", "Verified"
        REJECTED = "REJECTED", "Rejected"

    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=80, unique=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="verified_payments"
    )
    paid_at = models.DateTimeField(default=timezone.now)
    verified_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-paid_at"]

    def __str__(self):
        return f"{self.student.reg_number} - {self.reference}"


class Clearance(models.Model):
    student = models.OneToOneField("students.Student", on_delete=models.CASCADE, related_name="clearance")
    is_cleared = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    cleared_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="clearances"
    )
    cleared_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["student__reg_number"]

    def __str__(self):
        status = "Cleared" if self.is_cleared else "Not cleared"
        return f"{self.student.reg_number}: {status}"

# Create your models here.
