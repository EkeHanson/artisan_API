from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class EscrowTransaction(models.Model):
    TRANSACTION_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('FAILED', 'Failed'),
    ]

    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='buyer_transactions')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='seller_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=TRANSACTION_STATUS, default='PENDING')
    escrow_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Transaction {self.id} ({self.status})"




