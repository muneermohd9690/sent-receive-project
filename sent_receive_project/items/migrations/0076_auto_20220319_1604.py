# Generated by Django 3.1.2 on 2022-03-19 12:04

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0075_auto_20220319_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 16, 4, 38, 653687)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 16, 4, 38, 653687)),
        ),
    ]
