# Generated by Django 3.1.2 on 2022-03-19 09:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0063_auto_20220319_1342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 13, 45, 59, 522626)),
        ),
    ]
