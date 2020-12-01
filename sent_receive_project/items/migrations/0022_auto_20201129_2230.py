# Generated by Django 3.1.2 on 2020-11-29 18:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0021_auto_20201127_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 29, 22, 30, 41, 159544)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 29, 22, 30, 41, 159544)),
        ),
        migrations.AlterField(
            model_name='items',
            name='total_qty',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
    ]