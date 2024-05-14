# utils.py
from django.core.mail import send_mail
from django.conf import settings


def send_email_notification(subject, body, to_email):
    send_mail(subject, body, settings.EMAIL_HOST_USER, [to_email])
