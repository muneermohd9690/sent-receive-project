# Generated by Django 3.1.2 on 2020-11-15 19:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0008_auto_20201115_2059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 15, 23, 17, 26, 423063)),
        ),
    ]
