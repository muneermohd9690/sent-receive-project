# Generated by Django 3.1.2 on 2022-02-19 08:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0049_auto_20220219_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 19, 12, 39, 2, 559535)),
        ),
    ]
