# accounts/signals.py

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from .models import Users
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import datetime
from django.core.exceptions import ObjectDoesNotExist


# @receiver(post_save, sender=Users)
# def send_email_verification(sender, instance, created, **kwargs):
    
#     if created and not instance.email_verified:
#         verification_link = f"http://localhost:8000/verify_email/{instance.userID}/"
#         subject = 'Email Verification for Your Account'
#         message = f'Please click the link below to verify your email address:\n\n{verification_link}'
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [instance.email]
#         send_mail(subject, message, from_email, recipient_list)

# @receiver(post_save, sender=Users)
# def send_welcome_email(sender, instance, created, **kwargs):
#     if created and instance.email_verified:
#         subject = 'Doocumee Account Signup Activation Link'
#         message = f'Hello {instance.email},\n\nWelcome to our website! Thank you for joining us.'
#         from_email = settings.EMAIL_HOST_USER
#         recipient_list = [instance.email]
        
class AccountActivationView(APIView):
        def get(self, request, id, *args, **kwargs):
            
            try:
                user = Users.objects.get(userID=id)
       
                if not user:
                    return Response({'error': 'Account Activation Failed', 'message':'VERIFICATION_FAILED','statuscode':330}, status=status.HTTP_401_UNAUTHORIZED,)
            
                if not user.email_verified:
                    user.email_verified = True
                    user.save()
                    return Response({'statuscode': '200', 'message': 'VERIFID_SUCCESS',
                                    'userID':id, 
                                    'expireDate':datetime.datetime.now(),
                                    }, status=status.HTTP_200_OK)
                return Response({'error': 'Account Activation Already Done', 'message':'VERIFICATION_DONE','statuscode':320}, status=status.HTTP_401_UNAUTHORIZED,)
            
            except ObjectDoesNotExist:
                 return Response({'error': 'Account Activation Failed', 'message':'VERIFICATION_FAILED','statuscode':300}, status=status.HTTP_401_UNAUTHORIZED,)
            # do something
       