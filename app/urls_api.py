from django.urls import path
from rest_framework.routers import DefaultRouter
from app import (
    viewsets
)

api_urlpatterns = [
    path('api/upload/', viewsets.UploadAudioView.as_view(), name='upload_audio'),
]

audio_router = DefaultRouter()

audio_router.register(
    r'^api/audio',
    viewsets.AudioViewSet,
    basename="audio",
)

api_urlpatterns += audio_router.urls
process_router = DefaultRouter()

process_router.register(
    r'^api/process',
    viewsets.ProcessViewSet,
    basename="process"
)

api_urlpatterns += process_router.urls
