from django.db import models
from jobs.models import ServiceCategory
from users.models import CustomUser


class TradeReview(models.Model):
    
    service_category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, to_field='unique_id')

    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field='unique_id')


    reliability_rating = models.IntegerField(null=True, blank=True)
    workmanship_rating = models.IntegerField(null=True, blank=True)
    tidiness_rating = models.IntegerField(null=True, blank=True)
    courtesy_rating = models.IntegerField(null=True, blank=True)
    # overall_rating = models.IntegerField()
    review_title = models.CharField(max_length=255, null=True, blank=True)
    comment = models.TextField()
    value_of_work = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contact_name = models.CharField(max_length=255, null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    mobile_number = models.CharField(max_length=15, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.customer} on Simservice for {self.service_category.title}"
