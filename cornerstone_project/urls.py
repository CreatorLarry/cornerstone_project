"""
URL configuration for cornerstone_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

from main import views

urlpatterns = [
                  path('', views.home, name='home'),

                  path('about/', views.about, name='about'),

                  path('about/team/', views.team, name='team'),

                  path('about/testimonials/', views.testimonials, name='testimonials'),

                  path('about/pictorial/', views.pictorial, name='pictorial'),

                  path('sermon/', views.sermon, name='sermon'),

                  path('blog/', views.blog, name='blog'),

                  path("blog/<slug:slug>/", views.blog_detail, name="blog-detail"),

                  path("blog/<slug:slug>/comment/", views.add_comment, name="add_comment"),

                  path('events/', views.events, name='events'),

                  path('events/event-details/<int:event_id>/', views.event_details, name='event-details'),

                  path('departments/', views.departments, name='departments'),

                  path('departments/department-info', views.department_info, name='department-info'),

                  path('contact/', views.contact, name='contact'),

                  path('login/', views.login_member, name='login'),

                  path('logout/', views.logout_member, name='logout'),

                  path('new-member-registration/', views.new_member_registration, name='new-member-registration'),

                  path("password_reset/", auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
                       name="password_reset"),
                  path("password_reset/done/",
                       auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"),
                       name="password_reset_done"),
                  path("reset/<uidb64>/<token>/",
                       auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"),
                       name="password_reset_confirm"),
                  path("reset/done/",
                       auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
                       name="password_reset_complete"),

                  path('dashboard/', views.member_dashboard, name='member_dashboard'),

                  path('pie-chart', views.pie_chart, name='pie_chart'),

                  path('line-chart', views.line_chart, name='line_chart'),

                  path('bar-chart', views.bar_chart, name='bar_chart'),

                  path('member-details', views.member_details, name='member_details'),

                  path('profile-update', views.profile_update, name='update_profile'),

                  path('deposit-form', views.deposit_form, name='deposit_form'),

                  path('initiate-stk-push/', views.initiate_stk_push, name='initiate_stk_push'),

                  path("admin/deposit-report/", views.deposit_report, name="deposit_report"),

                  path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),

                  path('members/', views.members, name='members'),

                  path("events/upload/", views.upload_event, name="upload_event"),

                  path('register/<int:event_id>/', views.register_event, name='register_event'),

                  path("blogs/upload/", views.upload_blog, name="upload_blog"),

                  path("blogs/add-comment", views.add_comment, name="add_comment"),

                  path("sermons/upload/", views.upload_sermon, name="upload_sermon"),

                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
