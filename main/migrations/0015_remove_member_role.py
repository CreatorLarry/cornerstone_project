# Generated by Django 5.1.5 on 2025-02-24 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_member_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='role',
        ),
    ]
