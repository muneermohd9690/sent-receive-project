# Generated by Django 3.1.2 on 2020-11-27 06:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0036_auto_20201127_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 27, 10, 52, 33, 380633)),
        ),
    ]