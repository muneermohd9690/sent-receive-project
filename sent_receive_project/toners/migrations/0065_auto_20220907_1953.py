# Generated by Django 3.1.2 on 2022-09-07 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toners', '0064_auto_20220906_2028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tonerdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 7, 19, 52, 59, 466949)),
        ),
        migrations.AlterField(
            model_name='toners',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 7, 19, 52, 59, 465951)),
        ),
    ]
