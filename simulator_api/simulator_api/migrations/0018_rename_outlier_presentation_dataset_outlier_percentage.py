# Generated by Django 4.2.5 on 2023-09-13 09:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0017_rename_end_data_simulator_end_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dataset',
            old_name='outlier_presentation',
            new_name='outlier_percentage',
        ),
    ]