# Generated by Django 3.2 on 2022-08-15 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checklist', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='is_ok',
            field=models.BooleanField(default=True),
        ),
    ]
