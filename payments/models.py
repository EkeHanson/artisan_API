from django.db import models
from users.models import CustomUser

class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ('subscription', 'Subscription'),
        ('quote_acceptance', 'Quote Acceptance'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="payments")
    reference = models.CharField(max_length=100, unique=True)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)  # e.g., "success", "failed"
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.payment_type} - {self.status}"
