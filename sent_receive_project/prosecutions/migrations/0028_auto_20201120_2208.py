# Generated by Django 3.1.2 on 2020-11-20 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0027_auto_20201120_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 20, 22, 8, 15, 459966)),
        ),
    ]
