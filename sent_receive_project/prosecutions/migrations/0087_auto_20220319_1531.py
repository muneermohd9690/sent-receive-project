# Generated by Django 3.1.2 on 2022-03-19 11:31

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0086_auto_20220319_1530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 15, 31, 54, 369508)),
        ),
    ]
