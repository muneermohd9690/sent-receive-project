# Generated by Django 3.1.2 on 2022-03-19 14:29

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toners', '0017_auto_20220319_1417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tonerdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
        migrations.AlterField(
            model_name='toners',
            name='created',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]