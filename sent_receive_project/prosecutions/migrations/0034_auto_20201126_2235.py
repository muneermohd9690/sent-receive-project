# Generated by Django 3.1.2 on 2020-11-26 18:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0033_auto_20201125_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 26, 22, 35, 47, 453100)),
        ),
    ]
