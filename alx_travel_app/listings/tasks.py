from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_payment_confirmation_email(user_email, booking_id):
    subject = "Booking Payment Confirmation"
    message = f"Your payment for booking {booking_id} was successful. Thank you!"
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(subject, message, from_email, [user_email])

@shared_task
def send_payment_failed_email(user_email, booking_id):
    subject = "Payment Failed"
    message = f"Unfortunately, your payment for booking {booking_id} could not be completed."
    from_email = settings.DEFAULT_FROM_EMAIL

    send_mail(subject, message, from_email, [user_email])
