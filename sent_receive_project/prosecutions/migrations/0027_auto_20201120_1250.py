# Generated by Django 3.1.2 on 2020-11-20 08:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0026_auto_20201120_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 20, 12, 50, 54, 112137)),
        ),
    ]