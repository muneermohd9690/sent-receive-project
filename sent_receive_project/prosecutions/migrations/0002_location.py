# Generated by Django 3.1.2 on 2020-10-21 18:18

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('prosecutions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
    ]
