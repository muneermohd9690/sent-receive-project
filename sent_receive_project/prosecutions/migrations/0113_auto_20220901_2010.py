# Generated by Django 3.1.2 on 2022-09-01 16:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0112_auto_20220823_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 1, 20, 10, 20, 996757)),
        ),
    ]