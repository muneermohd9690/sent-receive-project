# Generated by Django 3.1.2 on 2020-11-25 17:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0031_auto_20201125_2139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 25, 21, 45, 58, 902087)),
        ),
    ]