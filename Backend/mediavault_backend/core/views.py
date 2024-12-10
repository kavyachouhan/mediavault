import uuid
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import login
from .models import User
from django.urls import reverse

def generate_verification_token():
    return str(uuid.uuid4())

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists'})
        
        # Generate verification token
        verification_token = generate_verification_token()
        
        # Create user
        user = User.objects.create_user(
            email=email,
            name=name,
            password=verification_token  # Temporary password
        )
        user.email_verification_token = verification_token
        user.save()
        
        # Send verification email
        verification_link = request.build_absolute_uri(
            reverse('verify_email', kwargs={'token': verification_token})
        )
        send_mail(
            'Verify Your MediaVault Account',
            f'Click the link to verify your account: {verification_link}',
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )
        
        return render(request, 'verification_sent.html')
    
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            user = User.objects.get(email=email)
            
            # Generate login token
            login_token = generate_verification_token()
            user.email_verification_token = login_token
            user.save()
            
            # Send login verification email
            login_link = request.build_absolute_uri(
                reverse('verify_login', kwargs={'token': login_token})
            )
            send_mail(
                'Login to MediaVault',
                f'Click the link to log in: {login_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            return render(request, 'login_verification_sent.html')
        
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Email not found'})
    
    return render(request, 'login.html')

def verify_email(request, token):
    try:
        user = User.objects.get(email_verification_token=token)
        user.is_verified = True
        user.email_verification_token = None
        user.save()
        
        login(request, user)
        return render(request, 'verification_success.html')
    
    except User.DoesNotExist:
        return render(request, 'verification_failed.html')

def verify_login(request, token):
    try:
        user = User.objects.get(email_verification_token=token)
        user.email_verification_token = None
        user.save()
        
        login(request, user)
        return redirect('home')
    
    except User.DoesNotExist:
        return render(request, 'login_failed.html')