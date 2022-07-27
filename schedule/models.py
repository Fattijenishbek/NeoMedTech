from django.db import models

from users.models import Doctor, Patient


class TimeSlots(models.Model):
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return f'{self.start} - {self.end}'


class WorkDays(models.Model):
    week_name = models.CharField(max_length=30)
    time_slots = models.ManyToManyField(TimeSlots)

    def __str__(self):
        return self.week_name


class Schedule(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    work_days = models.ManyToManyField(WorkDays)

    def __str__(self):
        return f'{self.doctor}'


class Appointment(models.Model):
    record = models.TextField(null=True)
    description = models.TextField(null=True)
    date = models.DateField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    time_slots = models.ManyToManyField(TimeSlots)

    def __str__(self):
        return f'{self.doctor} {self.date} {self.patient}'
