# Generated by Django 3.1.2 on 2022-03-19 15:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0078_auto_20220319_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 19, 47, 11, 75434)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 19, 47, 11, 75434)),
        ),
    ]
