from django import forms

from apps.accounts.models import User

from .models import Student


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ["user", "full_name", "reg_number", "programme", "year_of_study", "is_approved"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].queryset = User.objects.filter(role=User.Roles.STUDENT)
