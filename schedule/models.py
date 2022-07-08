from django.db import models
from users.models import Doctor, Patient


class Schedule(models.Model):
    work_date = models.ForeignKey("WorkDate",  blank=True, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.doctor}"


class WorkDate(models.Model):
    date = models.DateField()
    start = models.TimeField()
    end = models.TimeField()

    def __str__(self):
        return f"{self.date} {self.start} - {self.end}"


class Appointment(models.Model):
    disease = models.CharField(max_length=100)
    content = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=False)
    start_time = models.TimeField(auto_now_add=False)
    end_time = models.TimeField(auto_now_add=False)
    doctor = models.ForeignKey(Doctor, blank=True, null=True, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, blank=True, null=True, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.date} {self.start_time}"