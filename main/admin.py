from datetime import timedelta

from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.db import models

from ckeditor.widgets import CKEditorWidget
from django.utils import timezone
from import_export import resources
from import_export.admin import ExportMixin
from .models import AdminActivityLog, Notice, Project, ProjectImage, Comment

from .models import Message, AdminActivityLog
from main.models import Event, Sermon, Blog, EventRegistration, ContactMessage, LiveService

admin.site.site_header = "ACK Church Administration"
admin.site.site_title = "ACK Church Administration"

admin.site.unregister(User)


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('is_staff', 'is_active')

    fieldsets = (
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Authentication', {'fields': ('username', 'password')}),
    )

    add_fieldsets = (
        ('Personal Info', {'fields': ('username', 'first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Set Password', {'fields': ('password',)}),
    )

    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions')

    def save_model(self, request, obj, form, change):
        """Ensure password is properly hashed before saving."""
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])  # Hash the password
        super().save_model(request, obj, form, change)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location')


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'registered_on', 'contact')


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'preacher')


@admin.register(LiveService)
class LiveServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'date', 'preacher')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'sent_at')


class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'recipient', 'sent_at', 'is_read')


admin.site.register(Message, MessageAdmin)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date', 'posted_by')


class AdminActivityLogResource(resources.ModelResource):
    class Meta:
        model = AdminActivityLog
        fields = ('user__username', 'action', 'ip_address', 'timestamp')


class AdminActivityLogAdmin(admin.ModelAdmin):
    resource_class = AdminActivityLogResource
    list_display = ('user', 'action', 'ip_address', 'timestamp')
    list_filter = ('user', 'action', 'timestamp')
    search_fields = ('user__username', 'action', 'ip_address')

    def has_change_permission(self, request, obj=None):
        return False  # disables 'change' and removes history button


admin.site.register(AdminActivityLog, AdminActivityLogAdmin)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'action_flag', 'change_message')
    list_filter = ('user', 'action_flag', 'content_type')
    search_fields = ('object_repr', 'change_message')


admin.site.register(User, CustomUserAdmin)


class Last7DaysFilter(SimpleListFilter):
    title = 'last 7 days'
    parameter_name = 'last7days'

    def lookups(self, request, model_admin):
        return (('yes', 'Last 7 days'),)

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            last_week = timezone.now() - timedelta(days=7)
            return queryset.filter(timestamp__gte=last_week)


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at')
    inlines = [ProjectImageInline]

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'email')