# Generated by Django 3.1.2 on 2022-03-19 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toners', '0029_auto_20220319_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tonerdetails',
            name='created',
            field=models.DateTimeField(default='2022-19-03 15:02:46:15:02:46Z'),
        ),
        migrations.AlterField(
            model_name='toners',
            name='created',
            field=models.DateTimeField(default='2022-19-03 15:02:46'),
        ),
    ]