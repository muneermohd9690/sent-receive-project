# Generated by Django 3.1.2 on 2022-02-27 08:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toners', '0003_auto_20220221_2238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tonerdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 12, 29, 25, 266166)),
        ),
        migrations.AlterField(
            model_name='toners',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 27, 12, 29, 25, 266166)),
        ),
    ]