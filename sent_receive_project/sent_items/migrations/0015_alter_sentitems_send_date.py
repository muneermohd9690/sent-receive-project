# Generated by Django 5.0 on 2024-03-05 16:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sent_items', '0014_alter_sentitems_send_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sentitems',
            name='send_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 3, 5, 20, 44, 11, 704466)),
        ),
    ]
