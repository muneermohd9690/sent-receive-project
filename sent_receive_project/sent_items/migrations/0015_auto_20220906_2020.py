# Generated by Django 3.1.2 on 2022-09-06 16:20

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('sent_items', '0014_auto_20220906_1931'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='iproduct',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='tproduct',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='content_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='object_id',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='cart',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 6, 20, 20, 50, 529817)),
        ),
        migrations.AlterField(
            model_name='sentitems',
            name='send_date',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 6, 20, 20, 50, 530816)),
        ),
    ]
