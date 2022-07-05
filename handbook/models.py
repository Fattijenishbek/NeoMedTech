from email.mime import image
import imp
from django.db import models
from django.conf import settings

# Create your models here.

class HandBook(models.Model):
    week = models.IntegerField(default=1)
    title=models.CharField(max_length=250)
    image=models.ImageField()
    content=models.TextField()


class Todo(models.Model):
    task=models.CharField(max_length=250)
    done=models.BooleanField(default=False)
    date=models.DateTimeField(auto_now_add=False)
    # patient=models.ForeignKey(settings.User)

class Essentials(models.Model):
    name=models.CharField(max_length=250)
    done=models.BooleanField(default=False)
    #patient