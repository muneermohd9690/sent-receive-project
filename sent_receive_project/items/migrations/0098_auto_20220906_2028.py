# Generated by Django 3.1.2 on 2022-09-06 16:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0097_auto_20220906_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 6, 20, 28, 40, 222051)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 6, 20, 28, 40, 221051)),
        ),
    ]
