from django.db import models

from users.models import Doctor, Patient


class TimeSlots(models.Model):
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return f'{self.start} - {self.end}'


class Schedule(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.PROTECT, related_name='schedule')
    monday = models.ManyToManyField(TimeSlots, related_name='monday', blank=True)
    tuesday = models.ManyToManyField(TimeSlots, related_name='tuesday', blank=True)
    wednesday = models.ManyToManyField(TimeSlots, related_name='wednesday', blank=True)
    thursday = models.ManyToManyField(TimeSlots, related_name='thursday', blank=True)
    friday = models.ManyToManyField(TimeSlots, related_name='friday', blank=True)
    saturday = models.ManyToManyField(TimeSlots, related_name='saturday', blank=True)
    sunday = models.ManyToManyField(TimeSlots, related_name='sunday', blank=True)

    def __str__(self):
        return f'{self.doctor}'


class Appointment(models.Model):
    record = models.TextField(null=True)
    description = models.TextField(null=True)
    date = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name='appointment')
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, related_name='appointment')
    time_slots = models.ForeignKey(TimeSlots, on_delete=models.PROTECT, related_name='appointment')

    def __str__(self):
        return f'{self.doctor} {self.date} {self.patient}'



class Holidays(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT)
    day = models.DateField()

    def __str__(self):
        return f'{self.doctor} {self.day}'
