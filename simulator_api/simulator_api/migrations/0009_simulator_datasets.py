# Generated by Django 4.2.5 on 2023-09-07 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simulator_api', '0008_remove_simulator_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulator',
            name='datasets',
            field=models.JSONField(null=True),
        ),
    ]