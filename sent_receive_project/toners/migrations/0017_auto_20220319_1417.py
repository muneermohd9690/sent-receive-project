# Generated by Django 3.1.2 on 2022-03-19 10:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toners', '0016_auto_20220319_1354'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tonerdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 10, 17, 31, 750985)),
        ),
        migrations.AlterField(
            model_name='toners',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 19, 10, 17, 31, 750985)),
        ),
    ]
