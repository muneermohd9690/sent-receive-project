# Generated by Django 3.1.2 on 2022-04-08 18:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0081_auto_20220408_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 8, 22, 41, 59, 58557)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 8, 22, 41, 59, 57553)),
        ),
    ]
