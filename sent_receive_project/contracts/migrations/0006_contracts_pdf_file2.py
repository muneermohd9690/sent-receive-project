# Generated by Django 5.0 on 2024-03-05 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contracts', '0005_remove_contracts_employee_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracts',
            name='pdf_file2',
            field=models.FileField(blank=True, default='', null=True, upload_to='pdfs/items/'),
        ),
    ]
