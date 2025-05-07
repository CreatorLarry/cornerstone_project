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

                  path('departments/kayo-department', views.kayo_department, name='kayo-department'),
                  path('departments/kama-department', views.kama_department, name='kama-department'),
                  path('departments/mu-department', views.mu_department, name='mu-department'),
                  path('departments/children-department', views.children_department, name='children-department'),

                  path('contact/', views.contact_view, name='contact'),

                  path('register/<int:event_id>/', views.register_event, name='register_event'),

                  path("blogs/add-comment/", views.add_comment, name="add_comment"),

                  path("live-service/", views.live_service, name="live_service"),

                  path("notices/", views.notices, name="notices"),

                  path('notices/<int:pk>/', views.notice_details, name='notice-details'),

                  path('projects/', views.projects, name='projects'),

                  path('projects/<int:pk>/', views.project_detail, name='project-detail'),

                  path("giving/", views.giving, name="giving"),

                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
