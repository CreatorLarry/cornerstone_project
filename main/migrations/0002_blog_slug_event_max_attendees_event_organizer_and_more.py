# Generated by Django 5.1.5 on 2025-02-12 13:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AddField(
            model_name='event',
            name='max_attendees',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='event',
            name='organizer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='event',
            name='registration_required',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='member',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='role',
            field=models.CharField(choices=[('member', 'Member'), ('leader', 'Leader'), ('pastor', 'Pastor'), ('admin', 'Admin')], default='member', max_length=100),
        ),
        migrations.AddField(
            model_name='sermon',
            name='category',
            field=models.CharField(blank=True, choices=[('sunday_service', 'Sunday Service'), ('midweek_service', 'Midweek Service'), ('recorded', 'Recorded')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='sermon',
            name='duration',
            field=models.DurationField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='sermon',
            name='scripture_reference',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='blog_pictures'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='member',
            name='department',
            field=models.CharField(choices=[('kama', 'KAMA'), ('mothers_union', 'Mothers Union'), ('kayo', 'KAYO'), ('children', 'Children')], max_length=100),
        ),
        migrations.AlterField(
            model_name='member',
            name='dob',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='member',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], max_length=10),
        ),
        migrations.AlterField(
            model_name='member',
            name='groups',
            field=models.ManyToManyField(blank=True, related_name='member_groups', to='auth.group'),
        ),
        migrations.AlterField(
            model_name='member',
            name='profile_picture',
            field=models.ImageField(default='dashboard_assets/img/undraw_profile.svg', upload_to='profile_pictures'),
        ),
        migrations.AlterField(
            model_name='member',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, related_name='member_permissions', to='auth.permission'),
        ),
        migrations.AlterField(
            model_name='sermon',
            name='audio_file',
            field=models.FileField(blank=True, null=True, upload_to='sermon/'),
        ),
        migrations.AlterField(
            model_name='sermon',
            name='description',
            field=models.TextField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='sermon',
            name='preacher',
            field=models.CharField(max_length=100),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.blog')),
            ],
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(choices=[('Mobile Money', 'Mobile Money'), ('Cash', 'Cash')], default='Mobile Money', max_length=100)),
                ('amount', models.IntegerField()),
                ('status', models.CharField(choices=[('Paid', 'Paid'), ('Pending', 'Pending')], default='Pending', max_length=10)),
                ('date_paid', models.DateTimeField(auto_now_add=True)),
                ('paybill_number', models.CharField(blank=True, max_length=20, null=True)),
                ('account_number', models.CharField(blank=True, max_length=50, null=True)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='deposits', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'deposits',
            },
        ),
        migrations.CreateModel(
            name='EventRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('registered_on', models.DateTimeField(auto_now_add=True)),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='registrations', to='main.event')),
            ],
        ),
    ]
