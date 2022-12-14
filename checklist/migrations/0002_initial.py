# Generated by Django 3.2 on 2022-08-14 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('checklist', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medcard',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.patient'),
        ),
        migrations.AddField(
            model_name='checklisttemplate',
            name='title',
            field=models.ManyToManyField(to='checklist.Title'),
        ),
        migrations.AddField(
            model_name='checklist',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.doctor'),
        ),
        migrations.AddField(
            model_name='checklist',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='users.patient'),
        ),
        migrations.AddField(
            model_name='checklist',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='checklist.checklisttemplate'),
        ),
        migrations.AddField(
            model_name='answer',
            name='check_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answer', to='checklist.checklist'),
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='answer', to='checklist.question'),
        ),
    ]
