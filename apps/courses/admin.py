from django.contrib import admin

from .models import Course, Registration


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["code", "title", "department", "credit_units", "semester", "weekday", "start_time", "end_time"]
    search_fields = ["code", "title", "department"]
    list_filter = ["department", "semester", "weekday", "active"]
    filter_horizontal = ["prerequisites"]


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "semester", "registered_at"]
    search_fields = ["student__reg_number", "student__full_name", "course__code"]
    list_filter = ["semester", "course__department"]

# Register your models here.
