# Generated by Django 5.1.5 on 2025-03-19 08:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0023_alter_member_groups_alter_member_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deposit',
            name='member',
        ),
        migrations.RemoveField(
            model_name='member',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='member',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='SMSTemplate',
        ),
        migrations.DeleteModel(
            name='Deposit',
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]
