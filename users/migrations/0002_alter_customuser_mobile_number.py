# Generated by Django 5.1.4 on 2025-01-22 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
