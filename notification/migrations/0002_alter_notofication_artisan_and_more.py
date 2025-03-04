# Generated by Django 5.1.4 on 2025-02-28 15:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0003_jobrequest_admin_done_jobrequest_artisan_done_and_more'),
        ('notification', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notofication',
            name='artisan',
            field=models.ForeignKey(blank=True, limit_choices_to={'user_type': 'artisan'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.customuser', to_field='unique_id'),
        ),
        migrations.AlterField(
            model_name='notofication',
            name='customer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notification', to='users.customuser', to_field='unique_id'),
        ),
        migrations.AlterField(
            model_name='notofication',
            name='job_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='jobs.jobrequest', to_field='unique_id'),
        ),
    ]
