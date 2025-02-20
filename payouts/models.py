from django.db import models
from django.utils import timezone
from users.models import CustomUser
from jobs.models import JobRequest
import uuid


class Payouts(models.Model):

    ACCOUNT_CHOICES = [
        ('savings', 'Savings'),
        ('current', 'Current'),
    ]
        
    artisan = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        to_field='unique_id',
        limit_choices_to={'user_type': 'artisan'},
        db_index=True,
    )

    bank_name = models.CharField(max_length=255, blank=True, null=True)
    account_number = models.CharField(max_length=255, blank=True, null=True)
    account_name = models.CharField(max_length=255, blank=True, null=True)
    account_type = models.CharField(max_length=7, choices=ACCOUNT_CHOICES)


    def __str__(self):
        return f"{self.account_name} - {self.account_number} - {self.bank_name}"
