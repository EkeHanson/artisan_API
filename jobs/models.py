import uuid
from django.db import models
from users.models import CustomUser


class ServiceCategory(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Custom unique ID
    name = models.CharField(max_length=255, null=True, blank=True)
    postName = models.CharField(max_length=255, null=True, blank=True)
    simpleDescription = models.TextField(null=True, blank=True)
    complexDescription = models.TextField(null=True, blank=True)
    services = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.name} - {self.postName}"


class JobRequest(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="job_requests", to_field='unique_id')
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    budget = models.DecimalField(max_digits=10, decimal_places=2)

    service_description  = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    artisan = models.ForeignKey(
        CustomUser,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        to_field='unique_id',
        related_name="assigned_jobs"
    )
    status = models.CharField(
        max_length=50,
        choices=[('open', 'Open'), ('in_progress', 'In Progress'), ('completed', 'Completed')]
    )
    service_details = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        to_field='unique_id',
        related_name="job_requests"
    )
    issue_type = models.CharField(
        max_length=50,
        choices=[('simple', 'Simple'), ('complex', 'Complex')],
        default='simple'
    )
    attachments = models.FileField(upload_to='job_attachments/', null=True, blank=True)
    
    def __str__(self):
        return self.title



class Review(models.Model):
    job = models.OneToOneField(JobRequest, on_delete=models.CASCADE)
    customer = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="customer_reviews"
    )
    artisan = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="artisan_reviews"
    )
    rating = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

