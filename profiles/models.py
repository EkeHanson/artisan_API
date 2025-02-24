from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField  # Import ArrayField
from users.models import CustomUser
from jobs.models import ServiceCategory
import uuid
from datetime import datetime

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError

    ext = os.path.splitext(value.name)[1]  # Extract file extension
    valid_extensions = ['.png', '.jpg', '.jpeg', '.pdf']
    if ext.lower() not in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed formats: PNG, JPG, JPEG, PDF')



class ArtisanProfile(models.Model):
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        to_field='unique_id',
        limit_choices_to={'user_type': 'artisan'},
        db_index=True,
    )
    service_details = models.ForeignKey(
        ServiceCategory,
        on_delete=models.SET_NULL,
        to_field='unique_id',
        related_name="service_details",
        blank=True, null=True
    )

    user_image = models.FileField(upload_to='userImages/', null=True, blank=True, validators=[validate_file_extension])

    is_suspended = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    skills = models.JSONField(default=list)
    experience = models.PositiveIntegerField()
    business_name = models.CharField(max_length=255, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    certifications = models.CharField(max_length=255, blank=True, null=True)
    portfolio = models.JSONField(default=list)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    availability = models.JSONField(default=dict)

    qualifications = ArrayField(
        models.FileField(upload_to='qualifications/'),
        size=5,
        blank=True,
        null=True
    )
    previous_jobs = ArrayField(
        models.FileField(upload_to='previous_jobs/'),
        size=5,
        blank=True,
        null=True
    )

    identification_code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.user.user_type != 'artisan':
            raise ValidationError("The associated user must be of type 'artisan'.")
        if self.qualifications and len(self.qualifications) > 5:
            raise ValidationError("You can upload a maximum of 5 qualification files.")
        if self.previous_jobs and len(self.previous_jobs) > 5:
            raise ValidationError("You can upload a maximum of 5 qualification files.")

        # Generate identification code if not set
        if not self.identification_code:
            date_joined = self.user.date_joined
            month = date_joined.strftime("%m")  # Extract month as two digits
            year_last_two = date_joined.strftime("%y")  # Extract last two digits of the year
            user_id = self.user.id  # Get user ID
            
            self.identification_code = f"SSH{month}{year_last_two}{user_id}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"ArtisanProfile for {self.user.get_full_name()} ({self.user.email})"
