# Generated by Django 3.2 on 2022-08-18 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='officemanager',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='officemanager',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='last_name',
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]