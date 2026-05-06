from django.conf import settings
from django.db import models


class Notification(models.Model):
    class Kind(models.TextChoices):
        INFO = "INFO", "Info"
        SUCCESS = "SUCCESS", "Success"
        WARNING = "WARNING", "Warning"
        ERROR = "ERROR", "Error"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=120)
    message = models.TextField()
    kind = models.CharField(max_length=20, choices=Kind.choices, default=Kind.INFO)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

# Create your models here.
