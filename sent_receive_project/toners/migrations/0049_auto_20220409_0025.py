# Generated by Django 3.1.2 on 2022-04-08 20:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toners', '0048_auto_20220408_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tonerdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 9, 0, 24, 56, 60901)),
        ),
        migrations.AlterField(
            model_name='toners',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 9, 0, 24, 56, 59878)),
        ),
    ]
