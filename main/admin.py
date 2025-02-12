from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from main.models import Member, Event, Sermon, Blog, Deposit, EventRegistration


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    class MemberAdmin(admin.ModelAdmin):
        class Media:
            js = ('admin/js/autocomplete.js', 'admin/js/inlines.js')

    list_display = ('first_name', 'second_name', 'email', 'phone', 'date_joined', 'is_staff')
    search_fields = ('first_name', 'second_name', 'email', 'phone')
    list_filter = ('is_staff', 'is_active', 'date_joined')
    ordering = ('email',)

    # readonly_fields = ('date_joined', 'last_login')
    #
    # fieldsets = (
    #     ('Basic Info', {'fields': ('first_name', 'second_name', 'other_name', 'email', 'phone', 'profile_picture')}),
    #     ('Personal Information', {'fields': ('gender', 'dob', 'bio', 'department', 'role'), 'classes': ('collapse',)}),
    #     ('Permissions',
    #      {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions'), 'classes': ('collapse',)}),
    #     ('Important Dates', {'fields': ('last_login', 'date_joined'), 'classes': ('collapse',)}),
    # )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'first_name', 'second_name', 'email', 'phone', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'location')
    search_fields = ('title', 'location')

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ('name', 'event', 'registered_on')
    list_filter = ('event',)


@admin.register(Sermon)
class SermonAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'preacher')
    search_fields = ('title', 'preacher')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author')
    search_fields = ('title', 'author')

@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
    list_display = ('member', 'amount', 'date_paid', 'status')
    list_filter = ('status', 'date_paid')
    search_fields = ('member__first_name', 'member__second_name', 'amount')
