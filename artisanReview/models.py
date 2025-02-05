
from django.db import models
from users.models import CustomUser
from jobs.models import ServiceCategory  # Assuming this model exists

class ArtisanReview(models.Model):
    artisan = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        to_field='unique_id', 
        related_name="artisan_review_set",
        blank=True, 
        null=True
    )
    reviewer_name = models.ForeignKey(
        CustomUser, 
        on_delete=models.SET_NULL, 
        to_field='unique_id', 
        related_name="artisan_review_written_set",
        blank=True, 
        null=True  # Ensures reviewer_name is nullable
    )
    service_category = models.ForeignKey(
        ServiceCategory, 
        on_delete=models.SET_NULL, 
        related_name="artisan_service_reviews",
        to_field='unique_id', 
        blank=True, 
        null=True
    )
    rating = models.PositiveIntegerField()
    reliability_rating = models.PositiveIntegerField(blank=True, null=True)
    workmanship_rating = models.PositiveIntegerField(blank=True, null=True)
    tidiness_rating = models.PositiveIntegerField(blank=True, null=True)
    courtesy_rating = models.PositiveIntegerField(blank=True, null=True)
    review_title = models.CharField(max_length=255, blank=True, null=True)
    review_text = models.TextField(blank=True, null=True)
    value_of_work = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    date_of_experience = models.DateField(blank=True, null=True)
    contact_name = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating} stars review for {self.artisan} by {self.reviewer_name}"
