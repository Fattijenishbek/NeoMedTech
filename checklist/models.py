from django.db import models

# Create your models here.
class Schedule(models.Model):
    day_choices = (
        (1, 'Monday'),
        (2, 'Tuesday'),
        (3, 'Wednesday'),
        (4, 'Thursday'),
        (5, 'Friday'),
        (6, 'Saturday'),
        (7, 'Sunday')
    )
    working_days = models.PositiveIntegerField(choices=day_choices)
    start_time = models.TimeField()
    end_time = models.TimeField()
    # doctor = models.ForeignKey('Doctor', blank=True, null=True, on_delete=models.CASCADE)

