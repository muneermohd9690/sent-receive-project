# Generated by Django 3.1.2 on 2022-03-19 09:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0064_auto_20220319_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 13, 48, 12, 329404)),
        ),
    ]
