from django import forms

from .models import Clearance, Payment


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ["student", "amount", "reference", "status", "paid_at"]
        widgets = {"paid_at": forms.DateTimeInput(attrs={"type": "datetime-local"})}


class ClearanceForm(forms.ModelForm):
    class Meta:
        model = Clearance
        fields = ["student", "is_cleared", "notes"]
        widgets = {"notes": forms.Textarea(attrs={"rows": 3})}
