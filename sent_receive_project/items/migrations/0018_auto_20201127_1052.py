# Generated by Django 3.1.2 on 2020-11-27 06:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0017_auto_20201127_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 27, 10, 52, 33, 384653)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 27, 10, 52, 33, 383654)),
        ),
    ]
