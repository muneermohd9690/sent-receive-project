# Generated by Django 3.1.2 on 2020-11-19 19:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0013_auto_20201119_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 19, 23, 29, 40, 203937)),
        ),
    ]
