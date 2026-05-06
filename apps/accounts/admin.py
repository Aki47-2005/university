from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import AuditLog, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (("University Role", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("University Role", {"fields": ("role",)}),)
    list_display = ["username", "email", "role", "is_staff", "is_active"]
    list_filter = ["role", "is_staff", "is_active"]


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "timestamp", "ip_address"]
    list_filter = ["timestamp", "action"]
    search_fields = ["user__username", "action", "ip_address"]
    readonly_fields = ["user", "action", "timestamp", "ip_address"]

# Register your models here.
