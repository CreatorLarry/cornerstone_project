from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.db.models.aggregates import Sum
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from main.models import ContactMessage, EventRegistration, Event, Blog, Comment, Sermon
User = get_user_model()

import requests, base64, json, os
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from .mpesa_auth import get_access_token  # If you have it as a separate file
from .constants import DEPARTMENT_PAYBILLS
from cornerstone_project import settings
from twilio.rest import Client
import logging

logger = logging.getLogger(__name__)


# Basic views
def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


def team(request):
    return render(request, 'team.html')


def testimonials(request):
    return render(request, 'testimonials.html')


def pictorial(request):
    return render(request, 'pictorial.html')


def departments(request):
    return render(request, 'departments.html')


def department_info(request):
    return render(request, 'department-info.html')


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if name and email and subject and message:
            ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
            messages.success(request, "Your message has been sent. Thank you!")
            return redirect("contact")

    return render(request, "contact.html")

def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()

        if not name or not email:
            messages.error(request, "Name and Email are required.")
            return redirect("event-details", event_id=event.id)

        existing_registration = EventRegistration.objects.filter(event=event, email=email).exists()

        if existing_registration:
            messages.warning(request, "You have already registered for this event.")
        else:
            EventRegistration.objects.create(event=event, name=name, email=email)
            messages.success(request, "Registration successful!")

        return redirect("event-details", event_id=event.id)

    return redirect("event-details", event_id=event.id)  # Redirect if not post.

@csrf_exempt
def add_comment(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        content = request.POST.get("comment")

        if name and email and content:
            Comment.objects.create(
                blog=blog,
                name=name,
                email=email,
                content=content
            )

    return redirect("blog-detail", slug=blog.slug)


def kayo_department(request):
    return render(request, 'kayo_department.html')


def kama_department(request):
    return render(request, 'kama_department.html')


def mu_department(request):
    return render(request, 'mu_department.html')


def children_department(request):
    return render(request, 'children_department.html')



def live_service(request):
    return render(request, 'live_service.html')


from django.core.paginator import Paginator, EmptyPage


def sermon(request):
    sermons = Sermon.objects.all()
    paginator = Paginator(sermons, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sermon.html', {'sermons': sermons, 'page_obj': page_obj})


def blog(request):
    blogs = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog.html', {'blogs': blogs, 'page_obj': page_obj})


def events(request):
    events = Event.objects.all()
    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'events.html', {'events': events, 'page_obj': page_obj})


def blog_detail(request, slug):
    blog_post = get_object_or_404(Blog, slug=slug)
    comments = Comment.objects.filter(blog=blog_post)
    return render(request, 'blog-details.html', {'blog_post': blog_post, 'comments': comments})


def event_details(request, event_id):
    events = get_object_or_404(Event, id=event_id)
    return render(request, 'events-details.html', {'events': events})
