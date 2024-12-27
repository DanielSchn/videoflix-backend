from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from rest_framework.decorators import action
from django.conf import settings
from rest_framework import viewsets
from videoflix_app.models import Video, VideoProgress
from .serializers import VideoSerializer, VideoProgressSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import logging
from rest_framework.exceptions import NotAuthenticated


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    #@method_decorator(cache_page(CACHE_TTL))
    def list(self, request, *args, **kwargs):
        queryset = Video.objects.all()
        serializer = VideoSerializer(queryset, many=True)
        return Response(serializer.data)


    #@method_decorator(cache_page(CACHE_TTL))
    def retrieve(self, request, pk=None):
        video = Video.objects.get(pk=pk)
        serializer = VideoSerializer(video)
        return Response(serializer.data)
    

    def destroy(self, request, pk=None):
        video = Video.objects.get(pk=pk)
        video.delete()
        return Response({'message': 'Video deleted'}, status=204)
    

class VideoProgressViewSet(viewsets.ModelViewSet):
    serializer_class = VideoProgressSerializer
    queryset = VideoProgress.objects.all()
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return VideoProgress.objects.filter(user=user)
        else:
            raise NotAuthenticated('Unauthorized. Please log in.')
    

    @action(detail=False, methods=['get'])
    def get_user_progress(self, request):
        video_name = request.query_params.get('video_name')
        if not video_name:
            return Response({'error': 'video_name is required'}, status=status.HTTP_400_BAD_REQUEST)
        progress = self.get_queryset().filter(video_name=video_name).first()
        if progress:
            serializer = self.get_serializer(progress)
            return Response(serializer.data)
        else:
            return Response({'current_time': 0}, status=status.HTTP_200_OK)

    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)