# Generated by Django 3.1.2 on 2022-03-19 09:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toners', '0015_auto_20220319_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tonerdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 13, 54, 34, 951302)),
        ),
        migrations.AlterField(
            model_name='toners',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 13, 54, 34, 951302)),
        ),
    ]
