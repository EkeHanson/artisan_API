from django.db import models
from django.utils import timezone
from users.models import CustomUser
from jobs.models import JobRequest
import uuid




class QuoteRequest(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # ✅ Correct default UUID

    artisan = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        to_field='unique_id',
        limit_choices_to={'user_type': 'artisan'},
        db_index=True,
    )

    job_request = models.ForeignKey(
        JobRequest,
        on_delete=models.CASCADE,
        to_field='unique_id',
        db_index=True,
    )

    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    freelancer_service_fee = models.DecimalField(max_digits=10, decimal_places=2)
    job_duration = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['artisan', 'job_request'], name='unique_artisan_quote')
        ]

    def __str__(self):
        return f"{self.artisan} - {self.job_request} - {self.bid_amount}"



class Booking(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  
    quote = models.OneToOneField(QuoteRequest, on_delete=models.CASCADE, related_name="booking")
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field="unique_id", related_name="bookings")
    artisan = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field="unique_id", related_name="booked_jobs")
    job_request = models.ForeignKey(JobRequest, on_delete=models.CASCADE, to_field="unique_id", related_name="bookings")
    accepted_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=[
            ("pending", "Pending"),
            ("ongoing", "Ongoing"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
        ],
        default="pending"
    )

    def __str__(self):
        return f"Booking for {self.quote} - Status: {self.status}"
