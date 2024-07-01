# Generated by Django 5.0 on 2024-06-25 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0009_alter_contracts_warranty_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contracts',
            name='warranty_years',
            field=models.IntegerField(blank=True, choices=[(0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], default=0, null=True),
        ),
    ]
