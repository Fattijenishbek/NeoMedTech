from django.utils import timezone
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class SuperUser(BaseUserManager):
    def create_user(self, username, email, **extra_fields):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.set_unusable_password()
        user.save()
        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username=username,
            email=self.normalize_email(email),
            password=password,
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    user_type_choices = [
        ('doctor', 'doctor'),
        ('office_manager', 'office_manager'),
    ]
    username = models.CharField(max_length=255)
    email = models.EmailField(null=True, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    birth_date = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    user_type = models.CharField(max_length=255, choices=user_type_choices, default='admin')
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True, unique=True)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["username"]

    objects = SuperUser()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = 'System user'
        verbose_name_plural = "System users"


class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_pregnancy = models.DateField(auto_now_add=False, null=True, blank=True)
    inn = models.CharField(max_length=14)


    def __str__(self):
        return f'{self.user}'


class Doctor(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    resign = models.CharField(max_length=255)
    education = models.TextField()
    professional_sphere = models.TextField()
    work_experience = models.TextField()
    achievements = models.TextField()

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
