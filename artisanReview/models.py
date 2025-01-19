# # from django.db import models
# # from users.models import CustomUser

# # class ArtisanReview(models.Model):
# #     artisan = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,to_field='unique_id',related_name="customUser_details", blank=True, null=True )

# #     reviewer_name = models.ForeignKey(CustomUser,on_delete=models.SET_NULL,to_field='unique_id',related_name="customReviewer_details", blank=True, null=True )
    
# #     artisan_name = models.CharField(max_length=255)  # Artisan's name
# #     rating = models.PositiveIntegerField()  # Rating (1-5)
# #     review_text = models.TextField()  # Review text
# #     created_at = models.DateTimeField(auto_now_add=True)  # Auto timestamp

# #     def __str__(self):
# #         return f"{self.rating} stars review for {self.artisan_name}"



# from django.db import models
# from users.models import CustomUser
# from jobs.models import ServiceCategory  # Assuming this model exists

# class ArtisanReview(models.Model):
#     artisan = models.ForeignKey(
#         CustomUser, 
#         on_delete=models.SET_NULL, 
#         to_field='unique_id', 
#         related_name="artisan_review_set",  # Unique related_name
#         blank=True, 
#         null=True
#     )
#     reviewer_name = models.ForeignKey(
#         CustomUser, 
#         on_delete=models.SET_NULL, 
#         to_field='unique_id', 
#         related_name="artisan_review_written_set",  # Unique related_name
#         blank=True, 
#         null=True
#     )
#     service_category = models.ForeignKey(
#         ServiceCategory, 
#         on_delete=models.SET_NULL, 
#         related_name="artisan_service_reviews",  # Unique related_name
#         to_field='unique_id', 
#         blank=True, 
#         null=True
#     )
#     rating = models.PositiveIntegerField()  # Overall rating (1-5)
#     reliability_rating = models.PositiveIntegerField(blank=True, null=True)  # Reliability & timekeeping
#     workmanship_rating = models.PositiveIntegerField(blank=True, null=True)  # Quality of workmanship
#     tidiness_rating = models.PositiveIntegerField(blank=True, null=True)  # Tidiness
#     courtesy_rating = models.PositiveIntegerField(blank=True, null=True)  # Courtesy
#     review_title = models.CharField(max_length=255, blank=True, null=True)  # Review title
#     review_text = models.TextField(blank=True, null=True)  # Detailed review
#     value_of_work = models.DecimalField(
#         max_digits=10, 
#         decimal_places=2, 
#         blank=True, 
#         null=True
#     )  # Value of work completed in currency
#     date_of_experience = models.DateField(blank=True, null=True)  # Date of experience
#     contact_name = models.CharField(max_length=255, blank=True, null=True)  # Reviewer contact name
#     contact_email = models.EmailField(blank=True, null=True)  # Reviewer email
#     mobile_number = models.CharField(max_length=15, blank=True, null=True)  # Reviewer mobile number
#     created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of review creation

#     def __str__(self):
#         return f"{self.rating} stars review for {self.artisan} by {self.reviewer}"

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
