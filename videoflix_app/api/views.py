from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.conf import settings
from rest_framework import viewsets
from videoflix_app.models import Video
from .serializers import VideoSerializer
from rest_framework.response import Response


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)



class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

    @method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        queryset = Video.objects.all()
        serializer = VideoSerializer(queryset, many=True)
        return Response(serializer.data)


    @method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, pk=None):
        video = Video.objects.get(pk=pk)
        serializer = VideoSerializer(video)
        return Response(serializer.data)
    

    def destroy(self, request, pk=None):
        video = Video.objects.get(pk=pk)
        video.delete()
        return Response({"message": "Video deleted"}, status=204)