from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from .models import AuditLog


def get_client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


@receiver(user_logged_in)
def log_login(sender, request, user, **kwargs):
    AuditLog.objects.create(user=user, action="Logged in", ip_address=get_client_ip(request))


@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    if user and user.is_authenticated:
        AuditLog.objects.create(user=user, action="Logged out", ip_address=get_client_ip(request))


class AuditLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.client_ip = get_client_ip(request)
        return self.get_response(request)
