from django.urls import path, include
from django.conf.urls.static import static
from .views import VideoViewSet, VideoProgressViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'video', VideoViewSet, basename='video')
router.register(r'video-progress', VideoProgressViewSet, basename='video-progress')


urlpatterns = [
    path('', include(router.urls))
]