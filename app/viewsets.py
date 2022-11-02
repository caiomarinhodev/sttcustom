from rest_framework import viewsets, status

from django_filters import rest_framework as filters
from rest_framework.response import Response
from rest_framework.views import APIView

from . import (
    serializers,
    models
)

import django_filters

from .cloudinary_module import upload_audio
from .models import Audio, Process
from .stt_module import transcription_audio


class AudioFilter(django_filters.FilterSet):
    class Meta:
        model = models.Audio
        fields = ["id", "user__id", "filename"]


class AudioViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AudioSerializer
    queryset = models.Audio.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AudioFilter


class ProcessFilter(django_filters.FilterSet):
    class Meta:
        model = models.Process
        fields = ["id", "user__id", "audio__id", "status"]


class ProcessViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProcessSerializer
    queryset = models.Process.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProcessFilter


class UploadAudioView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            file = request.FILES['file']
            data = request.data
            language = data['language']
            result = upload_audio(file, file.name)
            audio = Audio()
            audio.filename = file.name
            audio.user = request.user
            audio.cloudinary_url = result['secure_url']
            audio.save()

            # download_file(os.path.join('audios', file.name), result['secure_url'])

            text = transcription_audio(file, lang=language, audio_type='wav')

            process = Process()
            process.user = request.user
            process.audio = audio
            process.status = 2
            process.result = text
            process.save()
            return Response({'message': 'ok', 'pk': process.pk}, status=status.HTTP_201_CREATED)
        except (Exception,):
            return Response({'message': 'error'}, status=status.HTTP_400_BAD_REQUEST)
