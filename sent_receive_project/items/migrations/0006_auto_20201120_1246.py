# Generated by Django 3.1.2 on 2020-11-20 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0005_auto_20201120_0036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemdetails',
            name='model_no',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='items.items'),
        ),
    ]
