# Generated by Django 3.1.2 on 2022-05-23 17:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0102_auto_20220409_0025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 5, 23, 21, 23, 19, 128993)),
        ),
    ]
