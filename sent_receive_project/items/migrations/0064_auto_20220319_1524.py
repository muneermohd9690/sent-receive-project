# Generated by Django 3.1.2 on 2022-03-19 11:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0063_auto_20220319_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 15, 24, 6, 496982)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 15, 24, 6, 496982)),
        ),
    ]
