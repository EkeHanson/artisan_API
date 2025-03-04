# Generated by Django 5.1.4 on 2025-02-25 16:53

import django.contrib.postgres.fields
import django.db.models.deletion
import profiles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArtisanProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_image', models.FileField(blank=True, null=True, upload_to='userImages/', validators=[profiles.models.validate_file_extension])),
                ('is_suspended', models.BooleanField(default=False)),
                ('is_subscribed', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=False)),
                ('skills', models.JSONField(default=list)),
                ('experience', models.PositiveIntegerField()),
                ('business_name', models.CharField(blank=True, max_length=255, null=True)),
                ('postcode', models.CharField(blank=True, max_length=20, null=True)),
                ('certifications', models.CharField(blank=True, max_length=255, null=True)),
                ('portfolio', models.JSONField(default=list)),
                ('hourly_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('availability', models.JSONField(default=dict)),
                ('about_artisan', models.TextField(blank=True, null=True)),
                ('business_location', models.CharField(blank=True, max_length=255, null=True)),
                ('proof_of_address', models.FileField(blank=True, null=True, upload_to='artisan_files/', validators=[profiles.models.validate_file_extension])),
                ('driver_licence', models.FileField(blank=True, null=True, upload_to='artisan_files/', validators=[profiles.models.validate_file_extension])),
                ('international_passport', models.FileField(blank=True, null=True, upload_to='artisan_files/', validators=[profiles.models.validate_file_extension])),
                ('NIN_doc', models.FileField(blank=True, null=True, upload_to='artisan_files/', validators=[profiles.models.validate_file_extension])),
                ('other_doc', models.FileField(blank=True, null=True, upload_to='artisan_files/', validators=[profiles.models.validate_file_extension])),
                ('qualifications', django.contrib.postgres.fields.ArrayField(base_field=models.FileField(upload_to='qualifications/'), blank=True, null=True, size=5)),
                ('previous_jobs', django.contrib.postgres.fields.ArrayField(base_field=models.FileField(upload_to='previous_jobs/'), blank=True, null=True, size=5)),
                ('service_details', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='service_details', to='jobs.servicecategory', to_field='unique_id')),
            ],
        ),
    ]
