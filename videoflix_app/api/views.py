from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.conf import settings
from rest_framework import viewsets
from videoflix_app.models import Video
from .serializers import VideoSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

#@cache_page(CACHE_TTL)
class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer


    @cache_page(CACHE_TTL)
    #@action(detail=False, methods=['get'])
    def get(self, request, *args, **kwargs):
        # Wenn du hier eine Cache-Abfrage machst, wird sie im Cache gespeichert
        queryset = Video.objects.all()
        return queryset