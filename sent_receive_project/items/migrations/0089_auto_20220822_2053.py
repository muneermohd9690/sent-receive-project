# Generated by Django 3.1.2 on 2022-08-22 16:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0088_auto_20220822_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 22, 20, 53, 13, 278528)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 22, 20, 53, 13, 278528)),
        ),
    ]