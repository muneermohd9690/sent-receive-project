# Generated by Django 3.1.2 on 2022-08-23 16:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0092_auto_20220822_2128'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 23, 20, 11, 24, 104593)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 23, 20, 11, 24, 104593)),
        ),
    ]