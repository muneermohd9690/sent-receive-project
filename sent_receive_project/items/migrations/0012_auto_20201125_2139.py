# Generated by Django 3.1.2 on 2020-11-25 17:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0011_auto_20201125_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 25, 21, 39, 32, 405497)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 25, 21, 39, 32, 404494)),
        ),
    ]
