# Generated by Django 3.1.2 on 2020-11-20 08:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0024_auto_20201120_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 20, 12, 46, 55, 668558)),
        ),
    ]
