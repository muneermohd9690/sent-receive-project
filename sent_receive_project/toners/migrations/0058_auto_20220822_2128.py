# Generated by Django 3.1.2 on 2022-08-22 17:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toners', '0057_auto_20220822_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tonerdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 22, 21, 28, 48, 847825)),
        ),
        migrations.AlterField(
            model_name='toners',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 22, 21, 28, 48, 847825)),
        ),
    ]
