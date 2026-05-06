from django.contrib import admin

from .models import Result


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ["student", "course", "semester", "grade", "uploaded_at"]
    search_fields = ["student__reg_number", "student__full_name", "course__code"]
    list_filter = ["semester", "grade"]

# Register your models here.
