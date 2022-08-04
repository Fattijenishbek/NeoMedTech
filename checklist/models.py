from django.db import models


from users.models import Patient, Doctor


class CheckList(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    pattern = models.ForeignKey("Pattern", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.patient}'


class Pattern(models.Model):
    titles = models.ManyToManyField("Title")
    recommendation = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.pk}'


class Title(models.Model):
    title = models.CharField(max_length=255)
    # check_list = models.ForeignKey(CheckList, on_delete=models.CASCADE, related_name='titles')

    def __str__(self):
        return f'{self.title}'


class Option(models.Model):
    title = models.ForeignKey(Title, on_delete=models.CASCADE, related_name="header")
    question = models.TextField()
    is_true = models.BooleanField(default=False)
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.question} - {self.answer}'


class MedCard(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    information = models.JSONField()

    def __str__(self):
        return f'{self.patient}'
