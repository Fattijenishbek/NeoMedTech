from django.db import models
from users.models import Patient, Doctor


class CheckList(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.pk} {self.doctor} - {self.patient}'


class Title(models.Model):
    check_list = models.ForeignKey(CheckList, related_name="titles", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    def __str__(self):
        return f'{self.title}'


class Option(models.Model):
    name = models.ForeignKey(Title, related_name='answers', on_delete=models.CASCADE)
    title = models.TextField()
    is_true = models.BooleanField(default=False)
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.title} - {self.answer}'


class MedCard(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    information = models.JSONField()

    def __str__(self):
        return f'{self.patient}'
