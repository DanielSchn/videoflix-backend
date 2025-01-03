from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status



User = get_user_model()

class UserTest(APITestCase):
    

    def setUp(self):
        
        self.admin = User.objects.create_superuser(
            username='admin@test.de', password='admin', email='admin@test.de', is_email_verified=True)
        self.user = User.objects.create_user(
            username='user@test.de', password='testpassword', email='user@test.de', is_email_verified=True)
        
        self.client = APIClient()


    # def test_user(self):
    #     print(User.objects.all())


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


    def test_register_user_short_password(self):
        url = reverse('registration')
        data = {
            "email": "daniel@daniel.de",
            "password": "safepa",
            "confirm_password": "safepa"
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["password"], ["Ensure this field has at least 8 characters."])


    def test_register_user_usermame_exists(self):
        url = reverse('registration')
        data = {
            "email": "user@test.de",
            "password": "safepassword",
            "confirm_password": "safepassword"
        }

        response = self.client.post(url, data, format='json')
        print('DATA',response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json()["email"], ["User with this email already exists."])


    def test_login(self):
        url = reverse('login')
        data = {
            "username": "user@test.de",
            "password": "testpassword"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "user@test.de")

    
    def test_login_wrong_password(self):
        url = reverse('login')
        data = {
            "username": "user@test.de",
            "password": "testpasword"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Wrong log in data.")


    def test_login_wrong_username(self):
        url = reverse('login')
        data = {
            "username": "use@test.de",
            "password": "testpassword"
        }

        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Wrong log in data.")