# Generated by Django 3.1.2 on 2022-03-19 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toners', '0032_auto_20220319_1522'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tonerdetails',
            name='created',
            field=models.DateTimeField(default='2022-24-03/19/22 15:24:0615:24:06Z'),
        ),
        migrations.AlterField(
            model_name='toners',
            name='created',
            field=models.DateTimeField(default='2022-24-03/19/22 15:24:0615:24:06Z'),
        ),
    ]