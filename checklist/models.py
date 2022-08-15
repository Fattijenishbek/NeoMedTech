from django.db import models
from users.models import Patient, Doctor


class CheckList(models.Model):
    MONTH_CHOICES = [
        (i, i) for i in range(1, 10)
    ]
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    month = models.SmallIntegerField(choices=MONTH_CHOICES, null=True)
    recommendations = models.TextField(blank=True)
    template = models.ForeignKey('CheckListTemplate', on_delete=models.PROTECT)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return f'Month: {self.month} ' \
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
    is_ok = models.BooleanField(default=True)
    question = models.ForeignKey(Question, on_delete=models.PROTECT, related_name='answer')
    check_list = models.ForeignKey(CheckList, on_delete=models.PROTECT, related_name='answer')

    def __str__(self):
        return f'{self.name} {self.question.name}'


class MedCard(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT)
    information = models.JSONField(null=True)
    is_archive = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.patient}'
