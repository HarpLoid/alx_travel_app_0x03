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

@shared_task
def send_booking_confirmation_email(user_email, booking_id, listing_name, total_price, start_date, end_date):
    """
    Task to send a booking confirmation email asynchronously
    """
    subject = f"Booking Confirmation - {listing_name}"
    message = (
        f"Dear {user_email},\n\n"
        f"Your booking has been successfully confirmed!\n\n"
        f"Booking Details:\n"
        f"Listing: {listing_name}\n"
        f"Start Date: {start_date}\n"
        f"End Date: {end_date}\n"
        f"Total Price: ₦{total_price}\n\n"
        f"Thank you for choosing us.\n\n"
        f"Best regards,\n"
        f"The Travel App Team"
    )

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

    return f"Booking confirmation email sent to {user_email}"
