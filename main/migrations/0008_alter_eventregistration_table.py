# Generated by Django 5.1.5 on 2025-02-13 07:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_eventregistration_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='eventregistration',
            table='main_eventregistrations',
        ),
    ]
