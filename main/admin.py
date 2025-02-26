from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path
from .models import Message, SMSTemplate

from main.models import Member, Event, Sermon, Blog, Deposit, EventRegistration, ContactMessage, LiveService
from main.utils import send_sms

admin.site.site_header = "ACK Church Administration"
admin.site.site_title = "ACK Church Administration"

if admin.site.is_registered(User):
    admin.site.unregister(User)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    class Media:
        js = ('admin/js/autocomplete.js', 'admin/js/inlines.js')

    list_display = ('first_name', 'second_name', 'email', 'phone', 'date_joined', 'is_staff', 'role')
    readonly_fields = ('role',)
    search_fields = ('first_name', 'second_name', 'email', 'phone')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    ordering = ('email',)

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:  # Allow superadmins to edit
            return ()
        return ('role',)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location', 'total_registrations')
    search_fields = ('title', 'location')

    def total_registrations(self, obj):
        return obj.registrations.count()

    total_registrations.short_description = 'Registrations'


@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'registered_on', 'contact', 'status')
    list_filter = ('event', 'status')
    search_fields = ('name', 'event__title', 'contact')

    def status(self, obj):
        return "✔️ Confirmed" if obj.confirmed else "❌ Pending"

    status.short_description = "Registration Status"


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'preacher', 'video_url')
    search_fields = ('title', 'preacher')
    list_filter = ('date', 'preacher')

    def sermon_length(self, obj):
        return f"{obj.length} mins" if obj.length else "N/A"

    sermon_length.short_description = 'Length'
@admin.register(LiveService)
class LiveService(admin.ModelAdmin):
    list_display = ('service_name', 'date', 'preacher', 'video_url')
    search_fields = ('service_name', 'preacher')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'author')


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'date_paid', 'status')
    list_filter = ('status', 'date_paid')
    search_fields = ('member__first_name', 'member__second_name', 'amount')
    actions = ['approve_selected', 'decline_selected']

    def approve_selected(self, request, queryset):
        queryset.update(status='Approved')
        self.message_user(request, "Selected deposits have been approved.")

    def decline_selected(self, request, queryset):
        queryset.update(status='Declined')
        self.message_user(request, "Selected deposits have been declined.")

    approve_selected.short_description = "Approve selected deposits"
    decline_selected.short_description = "Decline selected deposits"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'sent_at', 'mark_as_read')
    search_fields = ('name', 'email')
    actions = ['mark_selected_as_read']

    def mark_as_read(self, obj):
        return '✔️ Mark as Read'

    mark_as_read.allow_tags = True

    def mark_selected_as_read(self, request, queryset):
        queryset.update(is_read=True)

    mark_selected_as_read.short_description = 'Mark selected messages as read'


class CustomUserAdmin(UserAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can view users

    def has_add_permission(self, request):
        return request.user.is_superuser  # Only superusers can add users

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can edit users

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser  # Only superusers can delete users


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'recipient', 'sent_at', 'is_read')
    search_fields = ('subject', 'recipient__email')
    list_filter = ('is_read',)


@admin.register(SMSTemplate)
class SMSTemplateAdmin(admin.ModelAdmin):
    list_display = ('name',)


class BulkMessageAdmin(admin.ModelAdmin):
    change_list_template = "admin/bulk_messages.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send_bulk_messages/', self.admin_site.admin_view(self.send_bulk_messages), name="send_bulk_messages"),
        ]
        return custom_urls + urls

    def send_bulk_messages(self, request):
        if request.method == "POST":
            members = Member.objects.filter()
            message_content = request.POST.get("message")
            for member in members:
                if member.phone:
                    send_sms(member.phone, message_content)
            self.message_user(request, "Bulk messages sent successfully!")
            return HttpResponseRedirect("../")


admin.site.register(User, BulkMessageAdmin)

admin.site.register(User, CustomUserAdmin)
