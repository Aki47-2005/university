from django import forms

from .models import Course, Registration


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "code",
            "title",
            "credit_units",
            "department",
            "prerequisites",
            "weekday",
            "start_time",
            "end_time",
            "semester",
            "active",
        ]
        widgets = {
            "start_time": forms.TimeInput(attrs={"type": "time"}),
            "end_time": forms.TimeInput(attrs={"type": "time"}),
            "prerequisites": forms.CheckboxSelectMultiple,
        }


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ["course", "semester"]

    def __init__(self, *args, **kwargs):
        self.student = kwargs.pop("student")
        super().__init__(*args, **kwargs)
        self.fields["course"].queryset = Course.objects.filter(active=True)

    def clean(self):
        cleaned = super().clean()
        self.instance.student = self.student
        self.instance.course = cleaned.get("course")
        self.instance.semester = cleaned.get("semester")
        self.instance.full_clean(exclude=["student"] if self.instance.student_id else None)
        return cleaned
