# Generated by Django 4.2.5 on 2023-09-07 09:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0006_alter_simulator_datasets'),
    ]

    operations = [
        migrations.RenameField(
            model_name='simulator',
            old_name='datasets',
            new_name='data',
        ),
    ]
