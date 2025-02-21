from django.db import models

class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promo_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # description = models.TextField()
    features = models.JSONField(default=list)
    key_benefits = models.JSONField(default=list)

    def __str__(self):
        return self.name
