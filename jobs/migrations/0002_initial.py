# Generated by Django 5.1.4 on 2025-02-25 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequest',
            name='artisan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_jobs', to='users.customuser', to_field='unique_id'),
        ),
        migrations.AddField(
            model_name='jobrequest',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_requests', to='users.customuser', to_field='unique_id'),
        ),
        migrations.AddField(
            model_name='review',
            name='artisan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='artisan_reviews', to='users.customuser'),
        ),
        migrations.AddField(
            model_name='review',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_reviews', to='users.customuser'),
        ),
        migrations.AddField(
            model_name='review',
            name='job',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='jobs.jobrequest'),
        ),
        migrations.AddField(
            model_name='jobrequest',
            name='service_details',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_requests', to='jobs.servicecategory', to_field='unique_id'),
        ),
    ]
