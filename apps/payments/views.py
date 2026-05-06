from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from apps.accounts.decorators import staff_required
from apps.accounts.models import AuditLog
from apps.notifications.utils import notify

from .forms import ClearanceForm, PaymentForm
from .models import Clearance, Payment


@staff_required
def payment_list(request):
    query = request.GET.get("q", "")
    payments = Payment.objects.select_related("student", "verified_by")
    if query:
        payments = payments.filter(reference__icontains=query) | payments.filter(student__reg_number__icontains=query)
    page = Paginator(payments.distinct(), 10).get_page(request.GET.get("page"))
    return render(request, "payments/payment_list.html", {"page": page, "query": query})


@staff_required
def payment_create(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        payment = form.save()
        AuditLog.objects.create(user=request.user, action=f"Recorded payment {payment.reference}", ip_address=request.client_ip)
        notify(payment.student.user, "Payment recorded", f"Payment {payment.reference} has been recorded.", "INFO")
        messages.success(request, "Payment recorded.")
        return redirect("payment_list")
    return render(request, "form.html", {"form": form, "title": "Record Payment"})


@staff_required
def payment_update(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    old_status = payment.status
    form = PaymentForm(request.POST or None, instance=payment)
    if form.is_valid():
        payment = form.save(commit=False)
        if payment.status != old_status and payment.status == Payment.Status.VERIFIED:
            payment.verified_by = request.user
            payment.verified_at = timezone.now()
            notify(payment.student.user, "Payment confirmed", f"Payment {payment.reference} has been verified.", "SUCCESS")
        payment.save()
        AuditLog.objects.create(user=request.user, action=f"Updated payment {payment.reference}", ip_address=request.client_ip)
        messages.success(request, "Payment updated.")
        return redirect("payment_list")
    return render(request, "form.html", {"form": form, "title": "Edit Payment"})


@staff_required
def clearance_list(request):
    clearances = Clearance.objects.select_related("student", "cleared_by")
    page = Paginator(clearances, 10).get_page(request.GET.get("page"))
    return render(request, "clearance.html", {"page": page})


@staff_required
def clearance_update(request, pk):
    clearance = get_object_or_404(Clearance, pk=pk)
    form = ClearanceForm(request.POST or None, instance=clearance)
    if form.is_valid():
        clearance = form.save(commit=False)
        if clearance.is_cleared:
            clearance.cleared_by = request.user
            clearance.cleared_at = timezone.now()
            notify(clearance.student.user, "Financial clearance approved", "You are cleared for course registration.", "SUCCESS")
        else:
            clearance.cleared_by = request.user
            clearance.cleared_at = None
            notify(clearance.student.user, "Financial clearance pending", "Your clearance is not approved yet.", "WARNING")
        clearance.save()
        AuditLog.objects.create(user=request.user, action=f"Updated clearance for {clearance.student.reg_number}", ip_address=request.client_ip)
        messages.success(request, "Clearance updated.")
        return redirect("clearance_list")
    return render(request, "form.html", {"form": form, "title": "Update Clearance"})

# Create your views here.
