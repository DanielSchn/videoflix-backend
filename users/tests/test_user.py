from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status



User = get_user_model()

class UserTest(APITestCase):
    

    def setUp(self):
        
        self.admin = User.objects.create_superuser(
            username='admin', password='admin', email='admin@test.de', is_email_verified=True)
        self.user = User.objects.create_user(
            username='user', password='testpassword', email='user@test.de', is_email_verified=True)
        
        self.client = APIClient()


    def test_user(self):
        print(User.objects.all())


    def test_register_user(self):
        url = reverse('registration')
        data = {
            "email": "daniel@daniel.de",
            "password": "safepassword",
            "confirm_password": "safepassword"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Registration successful. Please check your email inbox to confirm your account.")


    def test_login(self):
        url = reverse('registration')