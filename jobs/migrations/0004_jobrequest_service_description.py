# Generated by Django 5.1.4 on 2025-01-22 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_jobrequest_attachments_jobrequest_job_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequest',
            name='service_description',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
