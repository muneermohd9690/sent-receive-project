# Generated by Django 5.0 on 2024-03-06 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0115_prosecutions_pdf_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prosecutions',
            name='pdf_file',
        ),
    ]
