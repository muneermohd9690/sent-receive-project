# Generated by Django 3.1.2 on 2022-04-08 20:25

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0082_auto_20220408_2242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 9, 0, 24, 56, 55172)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 4, 9, 0, 24, 56, 55172)),
        ),
    ]