# Generated by Django 3.1.2 on 2022-02-21 18:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0032_auto_20220221_2132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 21, 22, 38, 14, 657501)),
        ),
        migrations.AlterField(
            model_name='items',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2022, 2, 21, 22, 38, 14, 657501)),
        ),
    ]