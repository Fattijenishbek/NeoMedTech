# Generated by Django 3.2 on 2022-07-12 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('handbook', '0004_auto_20220712_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advices',
            name='week',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
