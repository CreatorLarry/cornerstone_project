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

import base64
from datetime import datetime

from cornerstone_project import settings
from .forms import ProfileUpdateForm
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from main.models import Member

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
from .models import Event, EventRegistration, Blog, Sermon
from .forms import EventForm, BlogForm, SermonForm
from django.contrib.auth.decorators import login_required


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
    return render(request, 'sermon.html', {'sermons': sermons})


def blog(request):
    blogs = Blog.objects.all().order_by('-created_at')  # Fetch blogs ordered by newest first
    paginator = Paginator(blogs, 6)  # Show 6 blogs per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'blog.html', {'page_obj': page_obj})


def events(request):
    events = Event.objects.all()  # Fetch all events
    return render(request, 'events.html', {'events': events})


def blog_detail(request, slug):
    blog_post = get_object_or_404(Blog, slug=slug)
    return render(request, 'blog-details.html', {'blog_post': blog_post})


def event_details(request):
    return render(request, 'events-details.html')


def departments(request):
    return render(request, 'departments.html')


def contact(request):
    return render(request, 'contact.html')


def department_info(request):
    return render(request, 'department-info.html')


def new_member_registration(request):
    if request.method == 'POST':
        form = MemberRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            member = form.save(commit=False)  # Don't save yet, modify first
            member.role = form.cleaned_data['role']
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
        phone_number = request.user.phone  # Ensure phone_number is valid

        # Validate inputs
        if not amount or not department:
            messages.error(request, "Invalid input. Amount and Department are required.")
            return redirect("deposit_form")

        # Get department's Paybill info
        paybill_info = DEPARTMENT_PAYBILLS.get(department, {})
        paybill_number = paybill_info.get("paybill", "")
        account_number = paybill_info.get("account_number", "")

        if not paybill_number or not account_number:
            messages.error(request, "Invalid department selected.")
            return redirect("deposit_form")

        # Generate Timestamp and Password
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password_str = f"{paybill_number}{settings.MPESA_PASSKEY}{timestamp}"
        password = base64.b64encode(password_str.encode()).decode()

        # Get M-Pesa Access Token
        access_token = get_access_token()
        if not access_token:
            messages.error(request, "Failed to get M-Pesa access token.")
            return redirect("deposit_form")

        # Construct STK Push Payload
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}

        payload = {
            "BusinessShortCode": paybill_number,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(amount),
            "PartyA": phone_number,
            "PartyB": paybill_number,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://yourdomain.com/mpesa/callback/",
            "AccountReference": account_number,
            "TransactionDesc": "Member Deposit"
        }

        # Send STK Push Request
        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()
        print(response_data)  # Debugging

        if response_data.get("ResponseCode") == "0":
            transaction_id = response_data.get("CheckoutRequestID")

            # Save deposit as "Pending"
            Deposit.objects.create(
                member=request.user.member,
                amount=amount,
                status="Pending",
                paybill_number=paybill_number,
                account_number=account_number,
                transaction_id=transaction_id
            )
            messages.success(request, "M-Pesa payment request sent! Please check your phone.")
        else:
            messages.error(request, "Failed to send M-Pesa request. Try again.")

        return redirect("deposit_form")


@login_required
@csrf_exempt
def mpesa_callback(request):
    try:
        data = json.loads(request.body)
        print(data)  # Debugging

        result_code = data["Body"]["stkCallback"]["ResultCode"]
        transaction_id = data["Body"]["stkCallback"].get("MpesaReceiptNumber", None)
        checkout_id = data["Body"]["stkCallback"]["CheckoutRequestID"]

        if result_code == 0 and transaction_id:
            deposit = Deposit.objects.get(transaction_id=checkout_id)
            deposit.status = "Paid"
            deposit.save()

            # Send SMS Notification
            send_sms_notification(deposit.member.phone, deposit.amount, transaction_id)

            return JsonResponse({"message": "Payment successful"}, status=200)
        else:
            return JsonResponse({"message": "Payment failed"}, status=400)

    except Exception as e:
        print("Callback Error:", str(e))  # Debugging
        return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def deposit_form(request):
    return render(request, 'deposit_form.html')


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
@login_required
def register_event(request, event_id):
    event = Event.objects.get(id=event_id)
    EventRegistration.objects.create(user=request.user, event=event)
    messages.success(request, f"You have successfully registered for {event.title}.")
    return redirect("events_list")


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
