from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError
from jobs.models import ServiceCategory

class ArtisanProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        to_field='unique_id',
        limit_choices_to={'user_type': 'artisan'}, # Restrict to Artisan users
        db_index=True,  # ✅ Improves query speed
    )
    # user = models.OneToOneField(
    #     CustomUser,
    #     on_delete=models.CASCADE,
    #     to_field='unique_id',
    #     limit_choices_to={'user_type': 'artisan'}  # Restrict to Artisan users
    # )
  
    service_details = models.ForeignKey(
    ServiceCategory,
    on_delete=models.SET_NULL,
    to_field='unique_id',  # Use the custom unique field
    related_name="service_details",
     blank=True, null=True
    )

    # skills = models.TextField()
    skills = models.JSONField(default=list)
    experience = models.PositiveIntegerField()
    location = models.CharField(max_length=255)

    postcode = models.CharField(max_length=20, blank=True, null=True)  # Added postcode field
    
    certifications = models.CharField(max_length=255, blank=True, null=True)
    portfolio = models.JSONField(default=list)  # Store URLs of images/videos
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    #service_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        # Validate that the user is an artisan
        if self.user.user_type != 'artisan':
            raise ValidationError("The associated user must be of type 'artisan'.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"ArtisanProfile for {self.user.get_full_name()} ({self.user.email})"

