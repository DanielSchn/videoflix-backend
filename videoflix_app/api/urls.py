from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import VideoViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'video', VideoViewSet, basename='video')


urlpatterns = [
    path('', include(router.urls))
]