from django.db import models
from users.models import Patient, Doctor


class CheckList(models.Model):
    MONTH_CHOICES = [
        (i, i) for i in range(1, 10)
    ]
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    month = models.SmallIntegerField(choices=MONTH_CHOICES, null=True)
    recommendations = models.TextField(blank=True)
    template = models.ForeignKey('CheckListTemplate', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Month: {self.month} ' \
               f'Doctor: {self.doctor} ' \
               f'Patient: {self.patient}'


class CheckListTemplate(models.Model):
    title = models.ManyToManyField('Title')


class Title(models.Model):
    name = models.CharField(max_length=256)
    question = models.ManyToManyField('Question')

    def __str__(self):
        return f'{self.name}'


class Question(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return f'{self.name}'


class Answer(models.Model):
    name = models.TextField(blank=True)
    is_ok = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, related_name='answer')
    check_list = models.ForeignKey(CheckList, on_delete=models.SET_NULL, null=True, related_name='answer')

    def __str__(self):
        return f'{self.name} {self.question.name}'


class MedCard(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    information = models.JSONField()

    def __str__(self):
        return f'{self.patient}'
