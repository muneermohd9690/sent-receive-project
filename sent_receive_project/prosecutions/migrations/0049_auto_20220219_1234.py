# Generated by Django 3.1.2 on 2022-02-19 08:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0048_auto_20220217_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 19, 12, 34, 42, 740261)),
        ),
    ]
