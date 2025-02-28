from django.db import models
from django.utils import timezone
from users.models import CustomUser
from jobs.models import JobRequest
import uuid




class Notofication(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # ✅ Correct default UUID

    artisan = models.ForeignKey( CustomUser,on_delete=models.CASCADE, to_field='unique_id',limit_choices_to={'user_type': 'artisan'},db_index=True, blank=True, null=True)
   
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, to_field="unique_id", related_name="notification", db_index=True, blank=True, null=True)

    job_request = models.ForeignKey(JobRequest,on_delete=models.CASCADE, to_field='unique_id',db_index=True, blank=True, null=True)

    notification_message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    notification_type = models.CharField(max_length=50, choices=[
        ('job_completed', 'Job Completed'),
        ('payment_made', 'Payment Made'),
        ('subscription_created', 'Subscription Created'),
    ])

    def __str__(self):
        return f"{self.user.unique_id} - {self.notification_type} - {self.message}"
