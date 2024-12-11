import uuid
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
from django.contrib.auth import login
from .models import User
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def generate_verification_token():
    return str(uuid.uuid4())

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'POST':
        try:
            email = request.POST.get('email')
            name = request.POST.get('name')
            
            if not email or not name:
                return JsonResponse({'error': 'Email and name are required'}, status=400)
            
            # Generate verification token
            verification_token = generate_verification_token()
            
            # Create user
            user = User.objects.create_user(
                email=email,
                name=name,
                password=verification_token
            )
            user.email_verification_token = verification_token
            user.save()
            
            # Build verification link
            verification_link = request.build_absolute_uri(
                reverse('verify_email', kwargs={'token': verification_token})
            )
            
            # Send verification email
            try:
                message = Mail(
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to_emails=email,
                    subject='Verify Your MediaVault Account',
                    html_content=f'<strong>Click to verify: <a href="{verification_link}">{verification_link}</a></strong>'
                )
                
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(message)
                
                logger.info(f"SendGrid Response: {response.status_code}")
                
                if response.status_code == 202:
                    return render(request, 'verification_sent.html')
                else:
                    raise Exception(f"SendGrid returned status code: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Email sending failed: {str(e)}")
                user.delete()  # Rollback user creation
                return JsonResponse({'error': 'Failed to send verification email'}, status=500)
                
        except Exception as e:
            logger.error(f"Signup failed: {str(e)}")
            return JsonResponse({'error': 'Signup failed'}, status=500)
    
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
            
            # Send verification email
            try:
                message = Mail(
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to_emails=email,
                    subject='Login to MediaVault',
                    html_content=f'Click the link to log in: {login_link}'
                )
                
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(message)
                
                logger.info(f"SendGrid Response: {response.status_code}")
                
                if response.status_code == 202:
                    return render(request, 'login_verification_sent.html')
                else:
                    raise Exception(f"SendGrid returned status code: {response.status_code}")
                    
            except Exception as e:
                logger.error(f"Email sending failed: {str(e)}")
                user.delete()  # Rollback user creation
                return JsonResponse({'error': 'Failed to send login email'}, status=500)
                
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