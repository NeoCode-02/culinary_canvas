# apps/users/tasks.py
from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.core.cache import cache
from .models import CustomUser
import random


@shared_task
def send_verification_email(user_id):
    try:
        user = CustomUser.objects.get(id=user_id)
        
        verification_code = str(random.randint(100000, 999999))
        
        cache.set(f"verification_code_{user.id}", verification_code, 120)

        subject = "Your Culinary Canvas Verification Code"
        message = f"""
        Hello {user.first_name},
        
        Your 6-digit verification code is: {verification_code}
        
        This code will expire in 2 minutes.
        
        Welcome to Culinary Canvas!
        """
        
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
    except CustomUser.DoesNotExist:
        print(f"User with id {user_id} not found.")