# Generated by Django 5.0 on 2024-03-05 17:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sent_items', '0023_alter_sentitems_send_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentitems',
            name='send_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 5, 21, 30, 37, 355511)),
        ),
    ]
