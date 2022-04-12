# Generated by Django 3.1.2 on 2022-04-08 18:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SentItems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('send_date', models.DateTimeField(default=datetime.datetime(2022, 4, 8, 22, 41, 59, 80460))),
                ('send_to', models.CharField(max_length=30)),
                ('product', models.CharField(max_length=30)),
                ('model_no', models.CharField(max_length=30)),
                ('serial_no', models.CharField(max_length=30)),
                ('received_by', models.CharField(max_length=30)),
            ],
        ),
    ]
