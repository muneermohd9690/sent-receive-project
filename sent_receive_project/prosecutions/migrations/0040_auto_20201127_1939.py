# Generated by Django 3.1.2 on 2020-11-27 15:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0039_auto_20201127_1208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 27, 19, 39, 35, 812493)),
        ),
    ]
