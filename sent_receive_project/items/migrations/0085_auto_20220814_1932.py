# Generated by Django 3.1.2 on 2022-08-14 15:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0084_auto_20220523_2123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 14, 19, 32, 12, 880880)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 14, 19, 32, 12, 879882)),
        ),
    ]