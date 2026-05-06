from django.contrib import admin

from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ["reg_number", "full_name", "programme", "year_of_study", "is_approved"]
    search_fields = ["reg_number", "full_name", "programme"]
    list_filter = ["programme", "year_of_study", "is_approved"]

# Register your models here.
