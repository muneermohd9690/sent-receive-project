# Generated by Django 3.1.2 on 2022-02-21 17:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toners', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tonerdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 21, 21, 31, 58, 71300)),
        ),
        migrations.AlterField(
            model_name='toners',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 21, 21, 31, 58, 70282)),
        ),
    ]
