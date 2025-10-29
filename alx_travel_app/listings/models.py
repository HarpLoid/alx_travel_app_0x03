from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import CheckConstraint, Q

class Listing(models.Model):
    listing_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    host = models.EmailField(unique=True, null=False)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    location = models.CharField(max_length=100, null=False)
    pricepernight = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    booking_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.EmailField(null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'),
                                                      ('confirmed', 'Confirmed'),
                                                      ('canceled', 'Canceled')],
                              default='pending', null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Booking {self.booking_id} for {self.user_email}'

class Review(models.Model):
    review_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user = models.EmailField(null=False)
    rating = models.IntegerField(null=False,
                                 validators=[MinValueValidator(1),
                                             MaxValueValidator(5)])
    comment = models.TextField(null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            CheckConstraint(
                check=Q(rating__gte=1) & Q(rating__lte=5),
                name='rating_range_check'
                )
        ]

    def __str__(self):
        return f'Review {self.review_id} for {self.listing_id}'

class Payment(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    payment_id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='payment')
    transaction_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Payment for Booking {self.booking.booking_id} - {self.payment_status}'
