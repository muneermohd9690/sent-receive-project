# Generated by Django 3.1.2 on 2022-03-19 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toners', '0024_auto_20220319_1442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tonerdetails',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='toners',
            name='created',
            field=models.DateTimeField(auto_now=True),
        ),
    ]