import uuid
import requests
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Listing, Booking, Payment
from .serializers import ListingSerializer, BookingSerializer
from rest_framework.permissions import AllowAny

class ListingViewSet(viewsets.ModelViewSet):
    """
    Manages Listing views
    """
    
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    
class BookingViewSet(viewsets.ModelViewSet):
    """
    Manages Bookings views
    """
    
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

class PaymentViewSet(viewsets.ViewSet):
    """
    Handles payment initiation through Chapa
    """

    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'], url_path='initiate')
    def initiate_payment(self, request):
        """
        Initiates payment by sending booking info to Chapa API.
        Stores transaction ID and sets initial status to Pending.
        """
        try:
            booking_id = request.data.get('booking_id')
            email = request.data.get('email')
            first_name = request.data.get('first_name', 'Guest')
            last_name = request.data.get('last_name', '')
            phone_number = request.data.get('phone_number', '')

            # Validate booking
            booking = Booking.objects.get(booking_id=booking_id)

            # Generate unique transaction reference
            transaction_ref = str(uuid.uuid4())

            # Prepare Chapa payload
            payload = {
                "amount": str(booking.total_price),
                "currency": "NGN",
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "tx_ref": transaction_ref,
                #"callback_url": "https://yourdomain.com/api/payment/verify/",
                "customization": {
                    "title": "Booking Payment",
                    "description": f"Payment for booking {booking_id}"
                }
            }

            headers = {
                "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}",
                "Content-Type": "application/json",
            }

            # Call Chapa API
            response = requests.post(settings.CHAPA_BASE_URL, json=payload, headers=headers)
            chapa_response = response.json()

            if response.status_code == 200 and chapa_response.get('status') == 'success':
                # Create Payment record
                Payment.objects.create(
                    booking=booking,
                    transaction_id=transaction_ref,
                    amount=booking.total_price,
                    payment_status='pending'
                )

                return Response({
                    "message": "Payment initiated successfully",
                    "checkout_url": chapa_response['data']['checkout_url'],
                    "transaction_id": transaction_ref
                }, status=status.HTTP_200_OK)

            return Response({
                "message": "Failed to initiate payment",
                "error": chapa_response
            }, status=status.HTTP_400_BAD_REQUEST)

        except Booking.DoesNotExist:
            return Response({"error": "Invalid booking ID"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], url_path='verify')
    def verify_payment(self, request):
        """
        Verifies payment with Chapa using the transaction ID.
        Updates Payment status accordingly.
        """
        tx_ref = request.query_params.get('tx_ref')

        if not tx_ref:
            return Response({"error": "Transaction reference (tx_ref) is required"}, status=status.HTTP_400_BAD_REQUEST)

        verify_url = f"https://api.chapa.co/v1/transaction/verify/{tx_ref}"

        headers = {
            "Authorization": f"Bearer {settings.CHAPA_SECRET_KEY}"
        }

        try:
            response = requests.get(verify_url, headers=headers)
            result = response.json()

            if result.get('status') == 'success' and result['data']['status'] == 'success':
                payment = Payment.objects.get(transaction_id=tx_ref)
                payment.payment_status = 'completed'
                payment.save()

                # send confirmation email asynchronously
                from .tasks import send_payment_confirmation_email
                send_payment_confirmation_email.delay(payment.booking.user, payment.booking.booking_id)

                return Response({
                    "message": "Payment verified successfully",
                    "payment_status": payment.payment_status
                }, status=status.HTTP_200_OK)
            else:
                payment = Payment.objects.filter(transaction_id=tx_ref).first()
                if payment:
                    payment.payment_status = 'failed'
                    payment.save()
                return Response({
                    "message": "Payment verification failed",
                    "details": result
                }, status=status.HTTP_400_BAD_REQUEST)

        except Payment.DoesNotExist:
            return Response({"error": "Payment record not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
