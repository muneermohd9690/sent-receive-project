# Generated by Django 5.0 on 2024-03-05 17:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0004_contracts_employee_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contracts',
            name='employee_number',
        ),
    ]