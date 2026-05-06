from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = "ADMIN", "Admin"
        STAFF = "STAFF", "Staff"
        STUDENT = "STUDENT", "Student"

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.STUDENT)

    @property
    def is_admin_role(self):
        return self.role == self.Roles.ADMIN or self.is_superuser

    @property
    def is_staff_role(self):
        return self.role in {self.Roles.ADMIN, self.Roles.STAFF} or self.is_superuser

    @property
    def is_student_role(self):
        return self.role == self.Roles.STUDENT


class AuditLog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        who = self.user.get_username() if self.user else "Anonymous"
        return f"{who}: {self.action}"

# Create your models here.
