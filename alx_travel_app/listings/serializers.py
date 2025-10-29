from rest_framework import serializers
from .models import Listing, Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['booking_id', 'listing_id', 'user', 'start_date',
                  'end_date', 'total_price', 'status', 'created_at']
        read_only_fields = ['booking_id', 'created_at']

class ListingSerializer(serializers.ModelSerializer):
    bookings = BookingSerializer(many=True, read_only=True, source='booking_set')
    
    class Meta:
        model = Listing
        fields = ['listing_id', 'host', 'name', 'description',
                  'location', 'pricepernight', 'created_at',
                  'updated_at', 'bookings']
        read_only_fields = ['listing_id', 'created_at', 'updated_at']
