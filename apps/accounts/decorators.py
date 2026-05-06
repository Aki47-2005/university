from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def role_required(*roles):
    def decorator(view_func):
        @login_required
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser or request.user.role in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You do not have permission to access that page.")
            return redirect("dashboard")

        return wrapper

    return decorator


def staff_required(view_func):
    return role_required("ADMIN", "STAFF")(view_func)


def admin_required(view_func):
    return role_required("ADMIN")(view_func)
