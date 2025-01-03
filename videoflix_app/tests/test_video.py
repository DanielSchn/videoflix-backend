from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from videoflix_app.models import Video
from datetime import datetime


User = get_user_model()


class VideoTest(APITestCase):
    
    def setUp(self):
        
        self.admin = User.objects.create_superuser(
            username='admin@test.de', password='admin', email='admin@test.de', is_email_verified=True)
        self.user = User.objects.create_user(
            username='user@test.de', password='testpassword', email='user@test.de', is_email_verified=True)
        
        self.token = Token.objects.create(user=self.user)
        
        self.client = APIClient()

#self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)



    def test_list_video_unauthenticated(self):
        url = reverse('video-list')

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")


    def test_list_video_authenticated(self):
        url = reverse('video-list')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_video_progress_unauthenticated(self):
        url = reverse('video-progress-list')

        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json()["detail"], "Authentication credentials were not provided.")


    def test_video_progress_authenticated(self):
        url = reverse('video-progress-list')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)