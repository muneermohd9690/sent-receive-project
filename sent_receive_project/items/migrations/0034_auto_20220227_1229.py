# Generated by Django 3.1.2 on 2022-02-27 08:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0033_auto_20220221_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 12, 29, 25, 266166)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 12, 29, 25, 266166)),
        ),
        migrations.AlterField(
            model_name='items',
            name='model_no',
            field=models.CharField(max_length=30, null=True, unique=True),
        ),
    ]
