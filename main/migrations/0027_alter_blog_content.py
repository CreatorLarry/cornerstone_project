# Generated by Django 5.1.5 on 2025-04-01 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_alter_event_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
    ]
