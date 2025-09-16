from django.db import models
import uuid

class PaymentMethod(models.Model):
    TYPE_CHOICES = [('CARD', 'Card'), ('PAYPAL', 'PayPal'), ('STRIPE', 'Stripe'),]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey('core.User', on_delete=models.CASCADE)
    pgw_token = models.CharField(max_length=255)
    last4 = models.CharField(max_length=4, blank=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)

class Payment(models.Model):
    STATE_CHOICES = [('PENDING', 'Pending'), ('AUTHORIZED', 'Authorized'), ('CAPTURED', 'Captured'), ('FAILED', 'Failed'), ('REFUNDED', 'Refunded'),]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default="USD")
    provider = models.CharField(max_length=255)
    transaction_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='PENDING')
    method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True)
    order = models.OneToOneField('services.OrderMicroservice', on_delete=models.SET_NULL, null=True, blank=True)
    session = models.OneToOneField('mentorship.MentorShipSession', on_delete=models.SET_NULL, null=True, blank=True)