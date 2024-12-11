from django.db import models
from users.models import CustomUser

class ArtisanReview(models.Model):
    artisan = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,to_field='unique_id',related_name="customUser_details", blank=True, null=True )

    reviewer_name = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,to_field='unique_id',related_name="customReviewer_details", blank=True, null=True )
    
    artisan_name = models.CharField(max_length=255)  # Artisan's name
    rating = models.PositiveIntegerField()  # Rating (1-5)
    review_text = models.TextField()  # Review text
    created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

    def __str__(self):
        return f"{self.rating} stars review for {self.artisan_name}"
