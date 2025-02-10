from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage
from django.db.models.aggregates import Sum
from django.http import JsonResponse
from .forms import ProfileUpdateForm
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from main.models import Member

User = get_user_model()

from django.shortcuts import render, redirect

from main.forms import MemberRegistrationForm

from .models import Deposit


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
    return render(request, 'sermon.html')


def blog(request):
    return render(request, 'blog.html')


def events(request):
    return render(request, 'events.html')


def blog_details(request):
    return render(request, 'blog-details.html')


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


def logout_member(request):
    logout(request)
    request.session.flush()
    messages.success(request, 'You have logged out successfully')
    return redirect("login")


@login_required(login_url='login')
def member_dashboard(request):
    deposits = Deposit.objects.filter(member=request.user)

    total_deposited = deposits.filter(status='Paid').aggregate(Sum('amount'))['amount__sum'] or 0
    expected_total = 200 if request.user.department == 'Mothers Union' or request.user.department == 'KAMA' else 100
    balance = expected_total - total_deposited if expected_total > total_deposited else 0

    # user = request.user
    # deposits = Deposit.objects.filter(member=user)

    context = {
        'deposits': deposits,
        'total_deposited': total_deposited,
        'balance': balance,
    }
    return render(request, 'dashboard.html', context)


def line_chart(request):
    deposits = Deposit.objects.filter(member=request.user).values('date_paid').annotate(total=Sum('amount')).order_by(
        'date_paid')

    labels = [deposit['date_paid'].strftime('%Y-%m-%d') for deposit in deposits]
    data = [deposit['total'] for deposit in deposits]

    return JsonResponse({'title': "Deposits Over Time", 'data': {'labels': labels, 'datasets': [
        {'label': 'KES Deposited', 'data': data, 'borderColor': '#4e73df', 'fill': False}]}})


def bar_chart(request):
    deposit_status = Deposit.objects.filter(member=request.user).values('status').annotate(total=Sum('amount'))

    labels = [deposit['status'] for deposit in deposit_status]
    data = [deposit['total'] for deposit in deposit_status]

    return JsonResponse({'title': "Deposits by Status", 'data': {'labels': labels, 'datasets': [
        {'label': 'KES Deposited', 'data': data, 'backgroundColor': ['#1cc88a', '#e74a3b']}]}})


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
    return render(request, 'member_details.html', {'user': request.user})


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
