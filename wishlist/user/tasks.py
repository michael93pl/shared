from celery import shared_task
from django.core.mail import EmailMessage

from wishlist import settings


@shared_task()
def send_system_mail(subject, message, receiver):

    email = EmailMessage(subject, message, to=[receiver])
    email.send()
