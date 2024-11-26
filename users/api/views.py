from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from .serializers import RegistrationSerializer, CustomUserSerializer
from django.contrib.auth import get_user_model
from rest_framework import status, generics
from django.core.exceptions import ValidationError
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.template.loader import render_to_string



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

            domain = get_current_site(request).domain
            verification_url = f'http://{domain}/api/verify-email/{uid}/{token}/'
            
            context = {
                'user': saved_account,
                'verification_url': verification_url,
            }
            subject = 'Bitte bestätigen Sie Ihre E-Mail-Adresse'
            from_email = 'Videoflix <noreply@dschneider-dev.de>'
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
                'message': 'Registrierung erfolgreich. Bitte prüfen Sie Ihr Emailpostfach zum bestätigen Ihres Accounts.',
                }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class VerifyEmailView(APIView):

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(get_user_model(), pk=uid)

            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.is_email_verified = True
                user.save()

                login(request, user)
                return Response({'message': 'Email bestätigt, Benutzer aktiv!'}, status=status.HTTP_200_OK)
            
            return Response({'error': 'Ungültiger Bestätigungscode!'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)