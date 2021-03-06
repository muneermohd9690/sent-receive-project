# Generated by Django 3.1.2 on 2020-11-29 18:32

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0022_auto_20201129_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 29, 22, 32, 55, 758717)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 29, 22, 32, 55, 758717)),
        ),
        migrations.AlterField(
            model_name='items',
            name='total_qty',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]
