# Generated by Django 5.1.5 on 2025-03-25 10:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_alter_blog_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='image',
            field=models.ImageField(default='events/default.jpg', upload_to='event_images/'),
        ),
    ]
