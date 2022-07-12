from django.db import models
from users.models import Patient, Doctor


class Question(models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.title}'


class Answer(models.Model):
    answer = models.CharField(max_length=256)
    is_ok = models.BooleanField(default=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.answer} - {self.question}'


class MedCard(models.Model):
    answer = models.ManyToManyField(Answer)
    recommendation = models.TextField(blank=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f'{self.recommendation}'


class CheckList(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    med_card = models.ForeignKey(MedCard, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.doctor} - {self.patient}'