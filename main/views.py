from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.core.paginator import Paginator, EmptyPage
from django.db.models.aggregates import Sum
from django.http import JsonResponse
from django.template.defaulttags import now
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now

from .forms import CommentForm, ContactForm

import base64
from datetime import datetime

from cornerstone_project import settings
from .forms import ProfileUpdateForm
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from main.models import Member, ContactMessage

User = get_user_model()

from django.shortcuts import render, redirect, get_object_or_404

from main.forms import MemberRegistrationForm

from .models import Deposit

from .mpesa_auth import get_access_token
from .constants import DEPARTMENT_PAYBILLS

from twilio.rest import Client
import os

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Event, EventRegistration, Blog, Sermon, Comment
from .forms import EventForm, BlogForm, SermonForm
from django.contrib.auth.decorators import login_required

import logging

logger = logging.getLogger(__name__)


# Create your views here.
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


def sermon(request):
    sermons = Sermon.objects.all()
    paginator = Paginator(sermons, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'sermon.html', {'sermons': sermons})


def blog(request):
    blogs = Blog.objects.all().order_by('-created_at')
    paginator = Paginator(blogs, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog.html', {'page_obj': page_obj})


def events(request):
    events = Event.objects.all()
    paginator = Paginator(events, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'events.html', {'events': events})


def blog_detail(request, slug):
    blog_post = get_object_or_404(Blog, slug=slug)
    comments = Comment.objects.filter(blog=blog_post)
    return render(request, 'blog-details.html', {'blog_post': blog_post, 'comments': comments})


def event_details(request, event_id):
    events = get_object_or_404(Event, id=event_id)
    return render(request, 'events-details.html', {'events': events})


def departments(request):
    return render(request, 'departments.html')


def contact_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        if name and email and subject and message:
            ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
            messages.success(request, "Your message has been sent. Thank you!")
            return redirect("contact")  # Prevents duplicate submissions on refresh

    return render(request, "contact.html")


def department_info(request):
    return render(request, 'department-info.html')


def new_member_registration(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)  # Don't save yet, modify first
            # member.role = form.cleaned_data['role']
            member.first_name = form.cleaned_data['first_name']
            member.second_name = form.cleaned_data['second_name']
            member.other_name = form.cleaned_data['other_name']
            member.phone = form.cleaned_data['phone']
            member.gender = form.cleaned_data['gender']
            member.dob = form.cleaned_data['dob']
            member.bio = form.cleaned_data['bio']
            member.department = form.cleaned_data['department']
            member.set_password(form.cleaned_data['password1'])  # Hash password
            member.save()  # Now save to database

            messages.success(request, 'Member Registration Successful. You can now Login')
            return redirect("login")
        else:
            print(form.errors)
            messages.error(request, 'Registration Failed. Please check the form and try again.')

    else:
        form = MemberRegistrationForm()
    return render(request, 'new-member-registration.html', {"form": form})


def login_member(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Email and password are required.")
            return render(request, 'login.html')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Login successful! Welcome to your dashboard.")
            return redirect('member_dashboard')
        else:
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, 'login.html')


@login_required
def logout_member(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'You have logged out successfully')
    return redirect("login")


@login_required(login_url='login')
def member_dashboard(request):
    deposits = Deposit.objects.filter(member=request.user)

    total_deposited = deposits.filter(status='Paid').aggregate(Sum('amount'))['amount__sum'] or 0
    expected_total = 200 * 12 if request.user.department == 'Mothers Union' or request.user.department == 'KAMA' else 100 * 12
    balance = expected_total - total_deposited if expected_total > total_deposited else 0

    # user = request.user
    # deposits = Deposit.objects.filter(member=user)

    context = {
        'deposits': deposits,
        'total_deposited': total_deposited,
        'balance': balance,
    }
    return render(request, 'dashboard.html', context)


@login_required
def line_chart(request):
    deposits = Deposit.objects.filter(member=request.user).values('date_paid').annotate(total=Sum('amount')).order_by(
        'date_paid')

    labels = [deposit['date_paid'].strftime('%Y-%m-%d') for deposit in deposits]
    data = [deposit['total'] for deposit in deposits]

    return JsonResponse({'title': "Deposits Over Time", 'data': {'labels': labels, 'datasets': [
        {'label': 'KES Deposited', 'data': data, 'borderColor': '#4e73df', 'fill': False}]}})


@login_required
def bar_chart(request):
    deposit_status = Deposit.objects.filter(member=request.user).values('status').annotate(total=Sum('amount'))

    labels = [deposit['status'] for deposit in deposit_status]
    data = [deposit['total'] for deposit in deposit_status]

    return JsonResponse({'title': "Deposits by Status", 'data': {'labels': labels, 'datasets': [
        {'label': 'KES Deposited', 'data': data, 'backgroundColor': ['#1cc88a', '#e74a3b']}]}})


@login_required
def pie_chart(request):
    deposit_types = Deposit.objects.filter(member=request.user).values('payment_method').annotate(total=Sum('amount'))

    labels = [deposit['payment_method'] for deposit in deposit_types]
    data = [deposit['total'] for deposit in deposit_types]

    return JsonResponse({
        'title': "Deposits by Payment Method",
        'data': {
            'labels': labels,
            'datasets': [{
                'data': data,
                'backgroundColor': ['#36b9cc', '#f6c23e']  # Colors for Mobile Money & Cash
            }]
        }
    })


@login_required
def members(request):
    data = Member.objects.all().order_by('id').values()  # ORM select * from members
    paginator = Paginator(data, 15)
    page = request.GET.get('page', 1)
    try:
        paginated_data = paginator.page(page)
    except  EmptyPage:
        paginated_data = paginator.page(1)
    return render(request, "members.html", {"data": paginated_data})


@login_required
def member_details(request):
    member = request.user
    return render(request, 'member_details.html', {'member': member})


@login_required
def profile_update(request):
    user = request.user

    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect("update_profile")  # Redirect back to the same page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, "profile_update.html", {"form": form})


@login_required(login_url='login')
def initiate_stk_push(request):
    if request.method == "POST":
        amount = request.POST.get("amount")
        department = request.POST.get("department")
        phone_number = request.user.member.phone  # Ensure correct phone field

        # Validate inputs
        if not amount or not department or not phone_number:
            messages.error(request, "Invalid input. Ensure all fields are filled.")
            return redirect("deposit_form")

        # Get department paybill info
        paybill_info = DEPARTMENT_PAYBILLS.get(department, {})
        paybill_number = paybill_info.get("paybill", settings.MPESA_EXPRESS_SHORTCODE)  # Use default if missing
        account_number = paybill_info.get("account_number", "ChurchDeposit")

        # Generate Timestamp & Password
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(
            f"{settings.MPESA_EXPRESS_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()).decode()

        # Get M-Pesa Access Token
        access_token = get_access_token()
        if not access_token:
            messages.error(request, "Failed to get M-Pesa access token.")
            return redirect("deposit_form")

        # STK Push Payload
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

        payload = {
            "BusinessShortCode": settings.MPESA_EXPRESS_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": settings.MPESA_EXPRESS_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://82f6-102-219-208-154.ngrok-free.app",
            "AccountReference": account_number,
            "TransactionDesc": "Church Member Deposit"
        }

        # Send STK Push Request
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        print("STK Response:", response_data)  # Debugging

        if response_data.get("ResponseCode") == "0":
            transaction_id = response_data.get("CheckoutRequestID")

            # Save deposit
            Deposit.objects.create(
                member=request.user.member,
                amount=amount,
                status="Pending",
                paybill_number=paybill_number,
                account_number=account_number,
                transaction_id=transaction_id
            )
            messages.success(request, "M-Pesa request sent! Check your phone.")
        else:
            messages.error(request, "Failed to send M-Pesa request. Try again.")

        return redirect("deposit_form")


def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    headers = {
        "Authorization": "Basic " + base64.b64encode(
            f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}".encode()
        ).decode()
    }

    response = requests.get(url, headers=headers)
    response_data = response.json()

    if "access_token" in response_data:
        return response_data["access_token"]

    print("Failed to get access token:", response_data)  # Debugging
    return None


@login_required
@csrf_exempt
def mpesa_callback(request):
    try:
        data = json.loads(request.body)
        logger.info(f"MPESA CALLBACK DATA: {data}")  # Log full callback data

        result_code = data["Body"]["stkCallback"]["ResultCode"]
        transaction_id = data["Body"]["stkCallback"].get("MpesaReceiptNumber") or data["Body"]["stkCallback"][
            "CheckoutRequestID"]
        checkout_id = data["Body"]["stkCallback"]["CheckoutRequestID"]

        logger.info(f"Result Code: {result_code}, Transaction ID: {transaction_id}, Checkout ID: {checkout_id}")

        if result_code == 0 and transaction_id:
            deposit = Deposit.objects.get(transaction_id=checkout_id)
            deposit.status = "Paid"
            deposit.save()
            logger.info(f"Deposit {deposit.id} marked as Paid")

            send_sms_notification(deposit.member.phone, deposit.amount, transaction_id)
            return JsonResponse({"message": "Payment successful"}, status=200)

        logger.warning("Payment failed or declined")
        return JsonResponse({"message": "Payment failed"}, status=400)

    except Exception as e:
        logger.error(f"Callback Error: {str(e)}")
        return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def deposit_form(request):
    if request.method == "POST":
        department = request.POST.get("department")
        amount = request.POST.get("amount")
        phone_number = request.POST.get("phone_number")

        if department and amount and phone_number:
            return JsonResponse({"success": True, "message": "Deposit request sent successfully! Check your phone for a prompt."})
        else:
            return JsonResponse({"success": False, "message": "Error processing deposit. Please try again."})

    return render(request, "deposit_form.html")


@login_required
def deposit_report(request):
    return render(request, 'deposit_report.html')


@login_required
def send_sms_notification(phone_number, amount, transaction_id):
    account_sid = os.getenv("TWILIO_ACCOUNT_SID")
    auth_token = os.getenv("TWILIO_AUTH_TOKEN")

    print("Twilio SID:", account_sid)  # Debugging
    print("Twilio Auth Token:", auth_token)

    if not account_sid or not auth_token:
        print("Twilio credentials missing")
        return

    client = Client(account_sid, auth_token)
    message = client.messages.create(
        body=f"Your deposit of {amount} KES was successful. Transaction ID: {transaction_id}",
        from_="+1234567890",
        to=phone_number,
    )

    return message.sid


# Upload an Event
@login_required
def upload_event(request):
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Event uploaded successfully!")
            return redirect("events_list")
    else:
        form = EventForm()
    return render(request, "events/upload.html", {"form": form})


# Register for an Event
def register_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()

        if not name:
            messages.error(request, "Name is required.")
            return redirect("event-details", event_id=event.id)

        if not email:
            messages.error(request, "Email is required.")
            return redirect("event-details", event_id=event.id)

        # Check if the email is already registered for this event
        existing_registration = EventRegistration.objects.filter(event=event, email=email).exists()

        if existing_registration:
            messages.warning(request, "You have already registered for this event.")
        else:
            # Create and save registration
            EventRegistration.objects.create(event=event, name=name, email=email)
            messages.success(request, "Registration successful!")

        return redirect("event-details", event_id=event.id)  # Redirect to event details

    return render(request, "events-details.html", {"event": event})


# Upload a Blog Post
@login_required
def upload_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post added!")
            return redirect("blog_list")
    else:
        form = BlogForm()
    return render(request, "blogs/upload.html", {"form": form})


# Upload a Sermon
@login_required
def upload_sermon(request):
    if request.method == "POST":
        form = SermonForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Sermon uploaded successfully!")
            return redirect("sermon_list")
    else:
        form = SermonForm()
    return render(request, "sermons/upload.html", {"form": form})


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


def custom_logout(request):
    logout(request)
    return redirect("/admin/login/")
