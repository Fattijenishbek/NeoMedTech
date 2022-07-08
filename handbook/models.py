from email.mime import image
from django.db import models
from django.conf import settings
from users.models import Patient
import datetime


# Create your models here.
class Todo(models.Model):
    task = models.CharField(max_length=255)
    done = models.BooleanField(default=False)
    date = models.DateField(default=datetime.date.today)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.task} - {self.patient}'


class Article(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()

    def __str__(self):
        return self.title


class Handbook(models.Model):
    week = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=128)
    content = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title


class Essentials(models.Model):
    title = models.CharField(max_length=128)
    done = models.BooleanField()
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
