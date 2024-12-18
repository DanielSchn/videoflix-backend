from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer, CustomUserSerializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.template.loader import render_to_string
import os
#from django.conf import settings


class UsersView(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()

            if not saved_account:
                raise ValidationError("Benutzer konnte nicht erstellt werden.")
            
            token = default_token_generator.make_token(saved_account)
            uid = urlsafe_base64_encode(str(saved_account.pk).encode())

            frontend_domain = os.environ.get('FRONTEND_DOMAIN')
            verification_url = f'{frontend_domain}/verify-email?uid={uid}&token={token}'
            
            context = {
                'user': saved_account,
                'verification_url': verification_url,
            }
            subject = 'Bitte bestätigen Sie Ihre E-Mail-Adresse'
            from_email = os.environ.get('DEFAULT_FROM_EMAIL')
            recipient_list = [saved_account.email]

            html_content = render_to_string('email_verification.html', context)
            text_content = f"""
            Hallo {saved_account.email},
            
            Vielen Dank für Ihre Registrierung! Bitte bestätigen Sie Ihre E-Mail-Adresse, indem Sie auf den folgenden Link klicken:
            
            {verification_url}
            
            Danke, dass Sie Videoflix nutzen!
            Das Videoflix-Team
            """

            email = EmailMultiAlternatives(subject, text_content, from_email, recipient_list)
            email.attach_alternative(html_content, 'text/html')
            email.send()

            return Response({
                'message': 'Registration successful. Please check your email inbox to confirm your account.',
                }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    User = get_user_model()
    
    def post(self, request, *arg, **kwarg):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = self.User.objects.get(username=username)
        except self.User.DoesNotExist:
            return Response({'detail': 'Wrong log in data.'}, status=status.HTTP_400_BAD_REQUEST)
        user = authenticate(request=request, username=user.username, password=password)
        if not user:
            return Response({'detail': 'Wrong log in data.'}, status=status.HTTP_400_BAD_REQUEST)
        data = {}
        token, created = Token.objects.get_or_create(user=user)
        data = {
            'token': token.key,
            'username': user.username,
            'user_id': user.id
        }
        return Response(data, status=status.HTTP_200_OK)
    

class VerifyEmailView(APIView):

    # def get(self, request, uidb64, token):
    #     try:
    #         uid = urlsafe_base64_decode(uidb64).decode()
    #         user = get_object_or_404(get_user_model(), pk=uid)

    #         if default_token_generator.check_token(user, token):
    #             user.is_active = True
    #             user.is_email_verified = True
    #             user.save()

    #             login(request, user)
    #         #    return Response({'message': 'Email bestätigt, Benutzer aktiv!'}, status=status.HTTP_200_OK)
    #             return render(request, 'success_verify.html', {'user': user})
            
    #         return Response({'error': 'Ungültiger Bestätigungscode!'}, status=status.HTTP_400_BAD_REQUEST)
        
    #     except Exception as e:
    #         return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')

        if not uid or not token:
            return Response({'error': ['UID und Token sind erforderlich.']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = get_object_or_404(get_user_model(), pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.is_email_verified = True
                user.save()

                return Response({'message': 'E-Mail erfolgreich bestätigt!'}, status=status.HTTP_200_OK)
            
            return Response({'error': 'Ungültiger Token.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': 'Ein Fehler ist aufgetreten.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequest(APIView):
    User = get_user_model()

    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'error': ['E-Mail Adresse benötigt.']})
        
        try:
            user = self.User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            reset_url = f'{os.environ.get('FRONTEND_DOMAIN')}/password-reset?uid={uid}&token={token}'

            subject = 'Reset password'
            from_email = os.environ.get('DEFAULT_FROM_EMAIL')
            recipent_list = [user.email]
            context = {
                'user' : user,
                'reset_url': reset_url
            }

            html_content = render_to_string('password_reset.html', context)
            text_content = f"""
            Hi {user.username},

            You've requested to reset your password. Please click on the following link: {reset_url}

            If you didn't request this, please ignore this email.

            Thank you,
            The Videoflix Team
            """

            email = EmailMultiAlternatives(subject, text_content, from_email, recipent_list)
            email.attach_alternative(html_content, 'text/html')
            email.send()

            return Response({'message': 'If the user exists, you will get an email with instructions.'}, status=status.HTTP_200_OK)
        
        except self.User.DoesNotExist:
            return Response({'message': 'If the user exists, you will get an email with instructions.'}, status=status.HTTP_200_OK)


class PasswordResetConfirm(APIView):
    User = get_user_model()

    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        if not uid or not token or not new_password:
            return Response({'error': 'All fields are required.'}, status=status.HTTP_400_BAD_REQUEST)
        

        try:
            user_id = urlsafe_base64_decode(uid).decode()
            user = self.User.objects.get(pk=user_id)

            token_generator = PasswordResetTokenGenerator()
            if token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password reset successful.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid or expired token.'}, status=status.HTTP_400_BAD_REQUEST)
            
        except self.User.DoesNotExist:
            return Response({'error': 'The specified user could not be found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)