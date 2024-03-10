# Generated by Django 5.0 on 2024-03-05 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prosecutions', '0114_alter_prosecutions_created_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='prosecutions',
            name='pdf_file',
            field=models.FileField(blank=True, default='', null=True, upload_to='pdfs/items/'),
        ),
    ]
