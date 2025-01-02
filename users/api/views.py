from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from .serializers import RegistrationSerializer, CustomUserSerializer
from django.contrib.auth import get_user_model, authenticate
from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator, PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
import os


class UsersView(generics.ListAPIView):
    """
    View to list all users in the system.

    This view is restricted to admin users only and uses the `ListAPIView` 
    from Django REST Framework to provide a read-only endpoint for listing users.
    """
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer


class RegistrationView(APIView):
    """
    View to handle user registration.

    This view allows new users to register an account. After successful registration, 
    an email verification link is sent to the user's email address.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user registration and send email verification.

        - Validates the data using the `RegistrationSerializer`.
        - Saves the user account as inactive.
        - Sends an email with a verification link.
        """
        serializer = RegistrationSerializer(data=request.data)
        data = {}

        if serializer.is_valid():
            saved_account = serializer.save()

            if not saved_account:
                raise ValidationError("User could not be created.")

            token = default_token_generator.make_token(saved_account)
            uid = urlsafe_base64_encode(str(saved_account.pk).encode())

            frontend_domain = os.environ.get('FRONTEND_DOMAIN')
            verification_url = f'{
                frontend_domain}/verify-email?uid={uid}&token={token}'

            context = {
                'user': saved_account,
                'verification_url': verification_url,
            }
            subject = 'Please confirm your email address.'
            from_email = os.environ.get('DEFAULT_FROM_EMAIL')
            recipient_list = [saved_account.email]

            html_content = render_to_string('email_verification.html', context)
            text_content = f"""
            Hello {saved_account.email},

            Thank you for signing up! Please confirm your email address by clicking on the following link:

            {verification_url}

            Thank you for using Videoflix!
            The Videoflix Team
            """

            email = EmailMultiAlternatives(
                subject, text_content, from_email, recipient_list)
            email.attach_alternative(html_content, 'text/html')
            email.send()

            return Response({
                'message': 'Registration successful. Please check your email inbox to confirm your account.',
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    View to handle user login.

    This view allows users to log in by providing their username and password. 
    If the credentials are correct, a token is returned to authenticate further requests.
    """
    permission_classes = [AllowAny]
    User = get_user_model()

    def post(self, request, *arg, **kwarg):
        """
        Handle user login.

        - Validates the username and password provided in the request data.
        - Authenticates the user and returns a token if credentials are correct.

        Returns:
            - 200 OK: On successful login, returns the token and user info.
            - 400 Bad Request: If the provided credentials are incorrect.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = self.User.objects.get(username=username)
        except self.User.DoesNotExist:
            return Response({'detail': 'Wrong log in data.'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            request=request, username=user.username, password=password)
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
    """
    View to verify the user's email address.

    This view is used to confirm the email address of a user by checking the
    validity of the provided UID (user ID) and token. If both are valid, the
    user's account is activated and their email is marked as verified.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle email verification process.

        - Decodes the UID and retrieves the user.
        - Checks the validity of the token.
        - Activates the user's account and verifies the email if the token is valid.
        """
        uid = request.data.get('uid')
        token = request.data.get('token')

        if not uid or not token:
            return Response({'error': ['UID and token are required.']}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = get_object_or_404(get_user_model(), pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.is_email_verified = True
                user.save()

                return Response({'message': 'Email successfully confirmed!'}, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': 'An error has occurred.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetRequest(APIView):
    """
    View to request a password reset email.

    This view handles the process of requesting a password reset. 
    It sends a reset email with a link that allows the user to change their password.
    """
    permission_classes = [AllowAny]
    User = get_user_model()

    def post(self, request):
        """
        Handle the password reset request.

        - Accepts the email address, validates its existence, and generates a reset token and UID.
        - Sends a password reset email to the user if the email exists.
        """
        email = request.data.get('email')

        if not email:
            return Response({'error': ['E-Mail Adresse benötigt.']})

        try:
            user = self.User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            reset_url = f'{os.environ.get(
                'FRONTEND_DOMAIN')}/password-reset?uid={uid}&token={token}'

            subject = 'Reset password'
            from_email = os.environ.get('DEFAULT_FROM_EMAIL')
            recipent_list = [user.email]
            context = {
                'user': user,
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

            email = EmailMultiAlternatives(
                subject, text_content, from_email, recipent_list)
            email.attach_alternative(html_content, 'text/html')
            email.send()

            return Response({'message': 'If the user exists, you will get an email with instructions.'}, status=status.HTTP_200_OK)

        except self.User.DoesNotExist:
            return Response({'message': 'If the user exists, you will get an email with instructions.'}, status=status.HTTP_200_OK)


class PasswordResetConfirm(APIView):
    """
    View to confirm and reset the user's password.

    This view handles the process of resetting the user's password. 
    It checks the validity of the provided UID and token, and if they are valid,
    the user's password is updated.
    """
    permission_classes = [AllowAny]
    User = get_user_model()

    def post(self, request):
        """
        Handle the password reset confirmation.

        - Accepts the UID, token, and new password.
        - Validates the token and updates the user's password if the token is valid.
        """
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


class TokenCheckView(APIView):
    """
    Endpoint to check if the provided token is valid.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Checks if the user is authenticated with a valid token.
        Returns true if the token is valid, otherwise false.
        """
        return Response({"valid": True}, status=200)