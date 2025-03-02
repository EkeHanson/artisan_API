from django.db import models
from users.models import CustomUser
from django.utils.timezone import now
from datetime import timedelta
from dateutil.relativedelta import relativedelta

import uuid



class SubscriptionPlan(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # description = models.TextField()
    features = models.JSONField(default=list)
    key_benefits = models.JSONField(default=list)

    def __str__(self):
        return self.name



class UserSubscription(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='unique_id')
    # subscribed_organization_address = models.CharField(max_length=100, null=True, blank=True)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True, to_field='unique_id')
    start_date = models.DateField(default=now)
    end_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    subscribing_user_name = models.CharField(max_length=100, null=True, blank=True)


    subscribed_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Amount paid by the user
    subscribed_duration = models.PositiveIntegerField(null=True, blank=True)  # Duration in months

    def save(self, *args, **kwargs):
        if not self.end_date and self.subscription_plan:
            # Calculate end_date based on subscribed_duration
            self.end_date = self.start_date + relativedelta(months=self.subscribed_duration)
        
        # Calculate the total amount if not provided
        if not self.subscribed_amount and self.subscription_plan:
            self.subscribed_amount = self.subscription_plan.price_per_month * self.subscribed_duration
        
        super().save(*args, **kwargs)
