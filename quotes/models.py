from django.db import models
from users.models import CustomUser


class QuoteRequest(models.Model):

    quoting_customer = models.ForeignKey(CustomUser, on_delete=models.SET_NULL,
    to_field='unique_id', related_name="quote_customer_set", blank=True, null=True)

    job_description = models.TextField()
    selected_trade = models.CharField(max_length=255)
    start_date_preference = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    profile_update = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return f"{self.full_name} - {self.selected_trade}"
