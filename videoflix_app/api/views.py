from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.decorators import action
from django.conf import settings
from rest_framework import viewsets
from videoflix_app.models import Video, VideoProgress
from .serializers import VideoSerializer, VideoProgressSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.exceptions import NotAuthenticated


CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class VideoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing video resources.

    This viewset provides CRUD operations (Create, Read, Update, Delete) for the `Video` model. It includes
    actions for listing all videos, retrieving individual videos, and deleting videos. It ensures that only
    authenticated users can perform these actions.

    Actions:
        - `list`: Returns a list of all video objects.
        - `retrieve`: Returns details of a single video.
        - `destroy`: Deletes a video.

    Permissions:
        - `IsAuthenticated`: Only authenticated users can access these views.

    Example Usage:
        - To get a list of videos:
            GET /videos/
        - To get the details of a specific video:
            GET /videos/{video_id}/
        - To delete a video:
            DELETE /videos/{video_id}/
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        """
        Overrides the permissions based on the action. 
        - list and retrieve: Only IsAuthenticated.
        - destroy: IsAdminUser, to ensure that only admins can delete. 
        """
        if self.action == 'destroy':
            return [IsAuthenticated(), IsAdminUser()]
        return super().get_permissions()

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
    """
    ViewSet for managing video progress resources.

    This viewset provides actions for tracking and retrieving a user's progress while watching videos.
    It allows users to get their progress on specific videos and store or update progress data.
    The `get_queryset` method filters the progress by the currently authenticated user.

    Actions:
        - `list`: Returns a list of all video progress entries for the current user.
        - `retrieve`: Retrieves details of a specific video progress entry (not implemented here).
        - `get_user_progress`: Returns the progress of the user for a specific video (e.g., current timestamp of where the user left off).
    
    Permissions:
        - `IsAuthenticated`: Only authenticated users can access these views.
    
    Example Usage:
        - To get a list of video progress for the logged-in user:
            GET /video-progress/
        - To get the user's progress for a specific video:
            GET /video-progress/get_user_progress/?video_name=some_video_name
    """
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