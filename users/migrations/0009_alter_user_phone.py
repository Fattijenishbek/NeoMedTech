# Generated by Django 3.2 on 2022-06-24 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20220624_2046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
