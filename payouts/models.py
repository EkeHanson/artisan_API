# from django.db import models
# from django.utils import timezone
# from users.models import CustomUser
# from jobs.models import JobRequest
# import uuid


# class Payouts(models.Model):
#     ACCOUNT_CHOICES = [
#         ('savings', 'Savings'),
#         ('current', 'Current'),
#     ]

#     artisan = models.OneToOneField(  # Enforces uniqueness at the DB level
#         CustomUser,
#         on_delete=models.CASCADE,
#         to_field='unique_id',
#         limit_choices_to={'user_type': 'artisan'},
#         db_index=True,
#     )

#     bank_name = models.CharField(max_length=255, blank=True, null=True)
#     account_number = models.CharField(max_length=255, blank=True, null=True)
#     account_name = models.CharField(max_length=255, blank=True, null=True)
#     account_type = models.CharField(max_length=7, choices=ACCOUNT_CHOICES)

#     def __str__(self):
#         return f"{self.account_name} - {self.account_number} - {self.bank_name}"
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser

class Payouts(models.Model):
    ACCOUNT_CHOICES = [
        ('savings', 'Savings'),
        ('current', 'Current'),
    ]

    artisan = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        to_field='unique_id',
        limit_choices_to={'user_type': 'artisan'},
        db_index=True,
    )

    bank_name = models.CharField(max_length=255, blank=True, null=True, default="Unknown Bank")
    account_number = models.CharField(max_length=255, blank=True, null=True, default="0000000000")
    account_name = models.CharField(max_length=255, blank=True, null=True, default="Unknown Name")
    account_type = models.CharField(max_length=7, choices=ACCOUNT_CHOICES, default="savings")

    def __str__(self):
        return f"{self.account_name} - {self.account_number} - {self.bank_name}"

# Auto-create a Payouts instance when an artisan is created
@receiver(post_save, sender=CustomUser)
def create_payouts_for_artisan(sender, instance, created, **kwargs):
    if created and instance.user_type == "artisan":
        Payouts.objects.create(artisan=instance)
