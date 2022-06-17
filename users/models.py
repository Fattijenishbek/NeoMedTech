from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractUser,
    BaseUserManager,
)


class SuperUser(BaseUserManager):
    def create_user(self, username, phone, password, **extra_fields):
        if not username:
            raise ValueError("User must have username")
        if not phone:
            raise ValueError("User must have phone number")
        if not password:
            raise ValueError("You need to come up with a password")
        user = self.model(
            username=username,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, phone, password):

        user = self.create_user(
            username=username,
            phone=phone,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.user_type = 'admin'
        user.save()
        return user


class User(AbstractUser):
    user_type_choices = [
        ('doctor', 'doctor'),
        ('patient', 'patient'),
        ('office_manager', 'office_manager'),
        ('admin', 'admin'),
    ]

    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    user_type = models.CharField(max_length=255, choices=user_type_choices, default='patient', null=True)
    address = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ["username"]

    objects = SuperUser()

    def __str__(self):
        return self.username


class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    month_of_pregnancy = models.DateField(auto_now_add=False, null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            if instance.user_type == 'patient':
                Patient.objects.create(user=instance)
            else:
                pass

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if instance.user_type == 'patient':
            instance.patient.save()
        else:
            pass

    def __str__(self):
        return f'{self.user}'


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    resign = models.PositiveSmallIntegerField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            if instance.user_type == 'doctor':
                Doctor.objects.create(user=instance)
            else:
                pass

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        if instance.user_type == 'doctor':
            instance.doctor.save()
        else:
            pass

    def __str__(self):
        return f'{self.user}'
