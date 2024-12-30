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

    Permissions:
        - Only accessible to users with admin privileges (`IsAdminUser`).

    Queryset:
        - Retrieves all user objects from the active user model (`get_user_model()`).

    Serializer:
        - Uses `CustomUserSerializer` to serialize the user data, exposing only 
          the `id`, `username`, and `email` fields.

    Example Usage:
        - Endpoint: `/api/users/`
        - Method: GET
    """
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer


class RegistrationView(APIView):
    """
    View to handle user registration.

    This view allows new users to register an account. After successful registration, 
    an email verification link is sent to the user's email address.

    Permissions:
        - Publicly accessible (`AllowAny`), meaning no authentication is required.

    Methods:
        - POST: Handles the registration process.

    Process:
        1. Validates the input data using `RegistrationSerializer`.
        2. Saves the user account and ensures it is inactive until email verification.
        3. Generates an email verification token and UID.
        4. Sends an email with the verification link to the user.

    Environment Variables:
        - FRONTEND_DOMAIN: The domain for the frontend application, used in the email verification link.
        - DEFAULT_FROM_EMAIL: The sender email address for the verification email.

    Example Usage:
        - Endpoint: `/api/register/`
        - Method: POST
        - Payload:
            {
                "email": "user@example.com",
                "password": "password123",
                "confirm_password": "password123"
            }
    
    Response:
        - 201 CREATED:
            {
                "message": "Registration successful. Please check your email inbox to confirm your account."
            }
        - 400 BAD REQUEST: If the provided data is invalid.

    Raises:
        - ValidationError: If the user account could not be created.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user registration and send email verification.

        - Validates the data using the `RegistrationSerializer`.
        - Saves the user account as inactive.
        - Sends an email with a verification link.

        Returns:
            - 201 Created: On successful registration.
            - 400 Bad Request: On invalid input data.
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
    """
    View to handle user login.

    This view allows users to log in by providing their username and password. 
    If the credentials are correct, a token is returned to authenticate further requests.

    Permissions:
        - Publicly accessible (`AllowAny`), meaning no authentication is required to log in.

    Methods:
        - POST: Handles the login process by validating the provided credentials and issuing a token.

    Process:
        1. Validates the `username` and `password` provided in the request data.
        2. Authenticates the user using Django's `authenticate` function.
        3. If authentication is successful, a token is generated or retrieved for the user.
        4. Returns the token along with the `username` and `user_id` in the response.

    Example Usage:
        - Endpoint: `/api/login/`
        - Method: POST
        - Payload:
            {
                "username": "user@example.com",
                "password": "password123"
            }

    Response:
        - 200 OK: On successful login, returns:
            {
                "token": "generated_token_key",
                "username": "user@example.com",
                "user_id": 1
            }
        - 400 BAD REQUEST: If the username or password is incorrect:
            {
                "detail": "Wrong log in data."
            }
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
    """
    View to verify the user's email address.

    This view is used to confirm the email address of a user by checking the
    validity of the provided UID (user ID) and token. If both are valid, the
    user's account is activated and their email is marked as verified.

    Permissions:
        - Publicly accessible (`AllowAny`), meaning no authentication is required.

    Methods:
        - POST: Verifies the user's email address by decoding the UID and validating the token.

    Process:
        1. Accepts a POST request with a `uid` (user ID) and a `token`.
        2. Decodes the `uid` and retrieves the user object.
        3. Validates the provided token.
        4. If valid, activates the user account and marks the email as verified.

    Example Usage:
        - Endpoint: `/api/verify-email/`
        - Method: POST
        - Payload:
            {
                "uid": "encoded_user_id",
                "token": "verification_token"
            }

    Response:
        - 200 OK: If email is successfully verified:
            {
                "message": "E-Mail erfolgreich bestätigt!"
            }
        - 400 BAD REQUEST: If UID or token are missing or invalid:
            {
                "error": "Ungültiger Token." or "UID und Token sind erforderlich."
            }
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle email verification process.

        - Decodes the UID and retrieves the user.
        - Checks the validity of the token.
        - Activates the user's account and verifies the email if the token is valid.

        Returns:
            - 200 OK: If the email is successfully verified.
            - 400 Bad Request: If the UID or token is missing, or the token is invalid.
        """
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
    """
    View to request a password reset email.

    This view handles the process of requesting a password reset. 
    It sends a reset email with a link that allows the user to change their password.

    Permissions:
        - Publicly accessible (`AllowAny`), meaning no authentication is required.

    Methods:
        - POST: Sends a password reset email to the user if the email exists.

    Process:
        1. Accepts a POST request with the user's email address.
        2. If the email exists, generates a password reset token and UID.
        3. Sends an email with the password reset link to the user.

    Environment Variables:
        - FRONTEND_DOMAIN: The domain for the frontend application, used in the password reset link.
        - DEFAULT_FROM_EMAIL: The sender email address for the password reset email.

    Example Usage:
        - Endpoint: `/api/password-reset-request/`
        - Method: POST
        - Payload:
            {
                "email": "user@example.com"
            }

    Response:
        - 200 OK: If the email exists or if the request is successfully processed:
            {
                "message": "If the user exists, you will get an email with instructions."
            }
    """
    permission_classes = [AllowAny]
    User = get_user_model()

    def post(self, request):
        """
        Handle the password reset request.

        - Accepts the email address, validates its existence, and generates a reset token and UID.
        - Sends a password reset email to the user if the email exists.

        Returns:
            - 200 OK: If the email exists or request is processed.
            - 400 Bad Request: If the email is not provided.
        """
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
    """
    View to confirm and reset the user's password.

    This view handles the process of resetting the user's password. 
    It checks the validity of the provided UID and token, and if they are valid,
    the user's password is updated.

    Permissions:
        - Publicly accessible (`AllowAny`), meaning no authentication is required.

    Methods:
        - POST: Confirms the password reset by validating the UID, token, and new password.

    Process:
        1. Accepts a POST request with the `uid` (user ID), `token` (reset token), and `new_password`.
        2. Decodes the `uid` and validates the token.
        3. If the token is valid, updates the user's password and returns a success message.

    Example Usage:
        - Endpoint: `/api/password-reset-confirm/`
        - Method: POST
        - Payload:
            {
                "uid": "encoded_user_id",
                "token": "reset_token",
                "new_password": "new_secure_password"
            }

    Response:
        - 200 OK: If the password is successfully reset:
            {
                "message": "Password reset successful."
            }
        - 400 BAD REQUEST: If the UID, token, or new password is invalid or missing:
            {
                "error": "All fields are required." or "Invalid or expired token."
            }
        - 404 NOT FOUND: If the user with the specified UID does not exist:
            {
                "error": "The specified user could not be found."
            }
    """
    permission_classes = [AllowAny]
    User = get_user_model()

    def post(self, request):
        """
        Handle the password reset confirmation.

        - Accepts the UID, token, and new password.
        - Validates the token and updates the user's password if the token is valid.

        Returns:
            - 200 OK: If the password is successfully reset.
            - 400 Bad Request: If any field is missing or the token is invalid.
            - 404 Not Found: If the user with the provided UID doesn't exist.
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

    permission_classes = [IsAuthenticated]  # Nur authentifizierte Benutzer können darauf zugreifen
    #authentication_classes = [TokenAuthentication]  # Nur Token Authentifizierung wird verwendet

    def get(self, request):
        """
        Überprüft, ob der Benutzer mit einem gültigen Token authentifiziert ist.
        Gibt `true` zurück, wenn der Token gültig ist, andernfalls `false`.
        """
        return Response({"valid": True}, status=200)