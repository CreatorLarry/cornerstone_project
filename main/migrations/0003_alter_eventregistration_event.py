# Generated by Django 5.1.5 on 2025-02-13 07:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_eventregistration_event'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventregistration',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registration', to='main.event'),
        ),
    ]
