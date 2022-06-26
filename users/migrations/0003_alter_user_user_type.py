# Generated by Django 3.2 on 2022-06-22 15:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20220622_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('doctor', 'doctor'), ('patient', 'patient'), ('office_manager', 'office_manager'), ('admin', 'admin')], default='admin', max_length=255, null=True),
        ),
    ]
