from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin, Permission, Group
from django.db import models

from django.conf import settings
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


# Create your models here.

# Member Manager Model
class MemberManager(BaseUserManager):
    def create_user(self, email, first_name, second_name, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, second_name=second_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, second_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, first_name, second_name, password, **extra_fields)


# Customer User Model
class Member(AbstractBaseUser, PermissionsMixin):
    username = None
    first_name = models.CharField(max_length=100)
    second_name = models.CharField(max_length=100)
    other_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=100, choices=(
        ('member', 'Member'), ('leader', 'Leader'), ('pastor', 'Pastor'), ('admin', 'Admin')), default='member')
    email = models.EmailField(max_length=100, unique=True)
    gender = models.CharField(max_length=10, choices=(('M', 'Male'), ('F', 'Female')))
    dob = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=100, choices=(
        ('kama', 'KAMA'), ('mothers_union', 'Mothers Union'), ('kayo', 'KAYO'), ('children', 'Children')))
    profile_picture = models.ImageField(upload_to='profile_pictures', default='dashboard_assets/img/undraw_profile.svg')
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        Group,
        related_name="member_groups",  # Fix conflict
        blank=True
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="member_permissions",  # Fix conflict
        blank=True
    )

    objects = MemberManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'second_name', 'phone']

    def __str__(self):
        return f"{self.first_name} {self.second_name} ({self.role})"


# Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog_pictures', default='dashboard_assets/img/undraw_blog.jpg', null=True, blank=True)

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


# Event Model
class Event(models.Model):
    title = models.CharField(max_length=100)
    organizer = models.ForeignKey(Member, on_delete=models.SET_NULL, null=True, blank=True)
    registration_required = models.BooleanField(default=False)
    max_attendees = models.IntegerField(default=0)
    date = models.DateTimeField()
    time = models.TimeField()
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='events/', default='events/default.jpg')

    def __str__(self):
        return self.title


class Deposit(models.Model):
    STATUS_CHOICES = [
        ('Paid', 'Paid'),
        ('Pending', 'Pending'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('Mobile Money', 'Mobile Money'),
        ('Cash', 'Cash'),
    ]

    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, default='Mobile Money')
    amount = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name='deposits')
    date_paid = models.DateTimeField(auto_now_add=True)
    paybill_number = models.CharField(max_length=20, blank=True, null=True)  # Stores department Paybill
    account_number = models.CharField(max_length=50, blank=True, null=True)  # Stores department Account No
    transaction_id = models.CharField(max_length=100, unique=True, blank=True, null=True)  # STK Push Transaction ID

    def __str__(self):
        return f"{self.member.first_name} - {self.amount} KES - {self.status}"

    class Meta:
        db_table = 'deposits'


class EventRegistration(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)