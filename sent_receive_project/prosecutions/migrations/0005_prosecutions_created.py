# Generated by Django 3.1.2 on 2020-11-04 16:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0004_auto_20201104_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='prosecutions',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 4, 20, 33, 2, 985822)),
        ),
    ]
