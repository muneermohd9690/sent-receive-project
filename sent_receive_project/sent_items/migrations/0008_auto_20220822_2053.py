# Generated by Django 3.1.2 on 2022-08-22 16:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sent_items', '0007_auto_20220822_2047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cartitem',
            old_name='send_to',
            new_name='issued_to',
        ),
        migrations.AlterField(
            model_name='cart',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 22, 20, 53, 13, 294152)),
        ),
        migrations.AlterField(
            model_name='sentitems',
            name='send_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 8, 22, 20, 53, 13, 294152)),
        ),
    ]
