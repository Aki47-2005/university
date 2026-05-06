from django.contrib import admin

from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "kind", "is_read", "created_at"]
    search_fields = ["user__username", "title", "message"]
    list_filter = ["kind", "is_read", "created_at"]

# Register your models here.
