from ckeditor.fields import RichTextField
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Permission, Group
from django.db import models

from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.

# Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_pictures', null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Auto-generate slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# Sermon Model
class Sermon(models.Model):
    title = models.CharField(max_length=100)
    preacher = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=100, choices=(
        ('sunday_service', 'Sunday Service'), ('midweek_service', 'Midweek Service'), ('recorded', 'Recorded')),
                                blank=True, null=True)
    scripture_reference = models.CharField(max_length=300, blank=True, null=True)
    duration = models.DurationField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    audio_file = models.FileField(upload_to='sermon/', blank=True, null=True)
    description = models.TextField(max_length=300, blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.preacher}"


class LiveService(models.Model):
    service_name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    preacher = models.CharField(max_length=50)
    start_time = models.TimeField()
    video_url = models.URLField(blank=True, null=True)  # Store YouTube link

    def embed_youtube(self):
        if self.video_url:
            video_id = self.video_url.split('v=')[-1]  # extract video id
            return f'https://www.youtube.com/watch?v={video_id}'
        return None

    def __str__(self):
        return f"{self.service_name}"


# Event Model
class Event(models.Model):
    title = models.CharField(max_length=100)
    organizer = models.CharField(max_length=100, blank=True, null=True)
    registration_required = models.BooleanField(default=False)
    max_attendees = models.IntegerField(default=0)
    date = models.DateTimeField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='event_images/', default='events/default.jpg')

    def __str__(self):
        return f"{self.title} - {self.date.strftime('%Y-%m-%d')}"


class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('pending', 'Pending'),
    ]
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contact = models.CharField(max_length=150, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.event.title}"

    class Meta:
        db_table = 'main_eventregistration'


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.name} on {self.blog}"

    from django.db import models


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True, null=True)
    subject = models.CharField(max_length=100)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"


class Message(models.Model):
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="messages")
    subject = models.CharField(max_length=100)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.subject} - {self.recipient.email}"


class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class AdminActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.timestamp}"

class Notice(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    posted_by = models.CharField(max_length=255)
    image = models.ImageField(upload_to='notice_images/', default='notices/default.jpg', blank=True, null=True)


class Project(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('planned', 'Planned'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    cover_image = models.ImageField(upload_to='project_covers/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ProjectImage(models.Model):
    project = models.ForeignKey(Project, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_photos/', null=True, blank=True)
    caption = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Image for {self.project.title}"
