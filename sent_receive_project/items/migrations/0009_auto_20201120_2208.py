# Generated by Django 3.1.2 on 2020-11-20 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0008_auto_20201120_1250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='itemdetails',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='itemdetails',
            name='date_updated',
        ),
        migrations.RemoveField(
            model_name='items',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='items',
            name='date_updated',
        ),
        migrations.AddField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 20, 22, 8, 15, 471962)),
        ),
        migrations.AddField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 20, 22, 8, 15, 470960)),
        ),
    ]
