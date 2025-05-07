# signals.py

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import AdminActivityLog


@receiver(user_logged_in)
def log_admin_login(sender, request, user, **kwargs):
    if user.is_staff:  # only track admin users
        ip = get_client_ip(request)
        AdminActivityLog.objects.create(
            user=user,
            action="Admin Logged In",
            ip_address=ip
        )


def log_admin_logout(sender, request, user, **kwargs):
    if user.is_staff:
        ip = get_client_ip(request)
        AdminActivityLog.objects.create(
            user=user,
            action="Admin Logged Out",
            ip_address=ip
        )


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
