from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import uuid
from django.utils import timezone
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]  # Extract file extension
    valid_extensions = ['.png', '.jpg', '.jpeg', '.pdf']
    if ext.lower() not in valid_extensions:
        raise ValidationError(f'Unsupported file extension. Allowed formats: PNG, JPG, JPEG, PDF')


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, phone, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')

        user_type = extra_fields.pop('user_type', 'customer')
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'super_admin')
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser):

    USER_TYPE_CHOICES = [
        ('artisan', 'Artisan'),
        ('customer', 'Customer'),
        ('super_admin', 'Super Admin'),
    ]

    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user_image = models.FileField(upload_to='userImages/', null=True, blank=True, validators=[validate_file_extension])

    user_type = models.CharField(max_length=11, choices=USER_TYPE_CHOICES)
    mobile_number = models.CharField(max_length=15, blank=True, null=True)
    is_verified = models.BooleanField(default=False)

    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups', blank=True)
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions', blank=True)

  
    # address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    is_subscribed = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    date_joined = models.DateTimeField(default=timezone.now)

    username = models.CharField(max_length=80, unique=False, blank=True, null=True)
    email = models.EmailField(max_length=80, unique=True)

    # Identification Code
    identification_code = models.CharField(max_length=20, unique=True, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name


    def save(self, *args, **kwargs):
        is_new = self._state.adding  # Check if the user is being created
        super().save(*args, **kwargs)  # Save initially

        if is_new and self.user_type == 'artisan' and not self.identification_code:
            self.identification_code = f"SSH{self.date_joined.strftime('%m')}{self.date_joined.strftime('%y')}{self.id}"
            super().save(update_fields=['identification_code'])
