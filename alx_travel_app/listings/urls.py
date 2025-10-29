from django.urls import path, include
from rest_framework import routers
from .views import ListingViewSet, BookingViewSet, PaymentViewSet

router = routers.DefaultRouter()
router.register('listings', ListingViewSet, basename='listing')
router.register('bookings', BookingViewSet, basename='booking')
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('', include(router.urls))
]
