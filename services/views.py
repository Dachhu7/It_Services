from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Service, Subscription
from .forms import UserRegistrationForm, OTPForm, ServiceForm, SubscriptionForm
import random
import razorpay

# Home view
# def home(request):
#     services = Service.objects.filter(active=True)
#     return render(request, 'home.html', {'services': services})
def home(request):
    services = Service.objects.all()  # Fetch all services, both active and inactive
    return render(request, 'home.html', {'services': services})

# User registration view
def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            otp = random.randint(100000, 999999)
            request.session['otp'] = otp
            request.session['user_data'] = form.cleaned_data
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [form.cleaned_data['email']],
                fail_silently=False,
            )
            return redirect('otp_confirmation')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# OTP confirmation view
def otp_confirmation_view(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            if int(form.cleaned_data['otp']) == request.session.get('otp'):
                user_data = request.session.get('user_data')
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                )
                login(request, user)
                return redirect('home')
    else:
        form = OTPForm()
    return render(request, 'otp_confirmation.html', {'form': form})

# User login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

# User logout view
def logout_view(request):
    logout(request)
    return redirect('home')

# Service CRUD views
@login_required
def create_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ServiceForm()
    return render(request, 'service_form.html', {'form': form})

@login_required
def service_detail(request, id):
    service = get_object_or_404(Service, id=id)
    return render(request, 'service_detail.html', {'service': service})

@login_required
def edit_service(request, id):
    service = get_object_or_404(Service, id=id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, request.FILES, instance=service)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'service_form.html', {'form': form})

@login_required
def delete_service(request, id):
    service = get_object_or_404(Service, id=id)
    service.delete()
    return redirect('home')

# Subscription success view
@login_required
def subscription_success(request):
    return render(request, 'subscription_success.html')

# Razorpay subscription view
@login_required
def subscribe(request, id):
    service = get_object_or_404(Service, id=id)
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.service = service
            total_price = service.price + (service.price * service.tax / 100)
            subscription.total_price = total_price
            subscription.save()

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
            payment = client.order.create({
                "amount": int(total_price * 100),  # Convert to paisa
                "currency": "INR",
                "payment_capture": "1"
            })
            subscription.transaction_id = payment['id']
            subscription.save()

            return render(request, 'subscription.html', {
                'service': service,
                'payment': payment,
                'subscription': subscription,
            })
    else:
        form = SubscriptionForm()
    return render(request, 'subscription.html', {'form': form, 'service': service})

# Payment callback view
@login_required
def payment_callback(request):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id')
        subscription_id = request.POST.get('subscription_id')

        subscription = get_object_or_404(Subscription, id=subscription_id)
        subscription.transaction_id = payment_id

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
        payment_details = client.payment.fetch(payment_id)

        if payment_details['status'] == 'captured':
            subscription.payment_status = 'Success'
            subscription.save()
            return redirect('subscription_success')
        else:
            subscription.payment_status = 'Failed'
            subscription.save()
            return redirect('subscription_failure')
    return redirect('home')

@login_required
def subscribe(request, id):
    service = get_object_or_404(Service, id=id)

    # Calculate price details
    price = service.price
    tax_rate = service.tax
    tax = price * tax_rate / 100
    total_price = price + tax

    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.service = service
            subscription.total_price = total_price
            subscription.save()

            # Razorpay configuration
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_SECRET_KEY))
            payment = client.order.create({
                "amount": int(total_price * 100),  # Convert to paisa
                "currency": "INR",
                "payment_capture": "1"
            })
            subscription.transaction_id = payment['id']
            subscription.save()

            return render(request, 'subscription.html', {
                'service': service,
                'price': price,
                'tax': tax,
                'total_price': total_price,
                'payment': payment,
                'subscription': subscription,
            })
    else:
        form = SubscriptionForm()

    return render(request, 'subscription.html', {
        'form': form,
        'service': service,
        'price': price,
        'tax': tax,
        'total_price': total_price,
    })
