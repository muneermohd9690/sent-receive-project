# Generated by Django 3.1.2 on 2020-11-25 17:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0012_auto_20201125_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 25, 21, 45, 58, 916322)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 25, 21, 45, 58, 916322)),
        ),
    ]
