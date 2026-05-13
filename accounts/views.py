import random
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import RegisterForm, LoginForm, ProfileUpdateForm

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    features = home_features()
    return render(request, "accounts/home.html", {"features": features})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )
            UserProfile.objects.create(
                user=user,
                role=form.cleaned_data.get('role', 'customer'),
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data.get('address', ''),
                date_of_birth=form.cleaned_data.get('date_of_birth'),
            )
            # Auto-create bank account
            from banking.models import BankAccount
            account_number = ''.join([str(random.randint(0,9)) for _ in range(12)])
            BankAccount.objects.create(user=user, account_number=account_number, balance=0.00)
            login(request, user)
            messages.success(request, f'Welcome {user.first_name}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })
    return render(request, 'accounts/profile.html', {'form': form})

# OTP simulation
otp_store = {}

def send_otp(request):
    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        otp = str(random.randint(100000, 999999))
        otp_store[phone] = otp
        request.session['otp_phone'] = phone
        request.session['otp_value'] = otp
        messages.info(request, f'OTP sent! (Simulation: {otp})')
        return redirect('verify_otp')
    return render(request, 'accounts/send_otp.html')

def verify_otp(request):
    if request.method == 'POST':
        entered = request.POST.get('otp', '')
        stored = request.session.get('otp_value', '')
        if entered == stored:
            messages.success(request, 'OTP verified successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'accounts/verify_otp.html')

def home_features():
    return [
        ('fa-exchange-alt', 'Money Transfer', 'Transfer funds instantly between accounts with OTP verification.'),
        ('fa-hand-holding-usd', 'Loan Management', 'Apply for personal, home, car, or education loans with EMI calculation.'),
        ('fa-chart-line', 'Transaction History', 'View detailed transaction history with filters and mini statements.'),
        ('fa-calculator', 'EMI Calculator', 'Calculate loan EMIs, total payable, and interest breakdown instantly.'),
        ('fa-address-book', 'Beneficiary Management', 'Save and manage your favourite transfer beneficiaries.'),
        ('fa-user-shield', 'Role-Based Access', 'Separate dashboards for Admin, Bank Employees, and Customers.'),
    ]
