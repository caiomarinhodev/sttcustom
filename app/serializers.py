from rest_framework import serializers


from app.models import Audio
class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = ("id", "user", "filename")


from app.models import Process
class ProcessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Process
        fields = ("id", "user", "audio", "status")


