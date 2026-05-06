from django.contrib import admin

from .models import Clearance, Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["student", "reference", "amount", "status", "paid_at", "verified_by"]
    search_fields = ["student__reg_number", "reference"]
    list_filter = ["status", "paid_at"]


@admin.register(Clearance)
class ClearanceAdmin(admin.ModelAdmin):
    list_display = ["student", "is_cleared", "cleared_by", "cleared_at"]
    search_fields = ["student__reg_number", "student__full_name"]
    list_filter = ["is_cleared", "cleared_at"]

# Register your models here.
