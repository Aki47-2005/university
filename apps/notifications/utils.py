from .models import Notification


def notify(user, title, message, kind=Notification.Kind.INFO):
    if user:
        Notification.objects.create(user=user, title=title, message=message, kind=kind)
