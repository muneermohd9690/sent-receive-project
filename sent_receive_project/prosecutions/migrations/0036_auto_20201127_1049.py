# Generated by Django 3.1.2 on 2020-11-27 06:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0035_auto_20201126_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 27, 10, 49, 7, 235548)),
        ),
    ]
