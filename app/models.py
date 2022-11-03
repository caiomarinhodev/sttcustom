import uuid

from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Audio(Timestamp):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255, blank=True, null=True)
    cloudinary_url = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.filename


STATUS_PROCESS = (
    (1, 'Processing'),
    (2, 'Completed'),
    (0, 'Failed'),
)


class Process(Timestamp):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    audio = models.ForeignKey(Audio, blank=True, null=True, on_delete=models.CASCADE)
    language = models.CharField(max_length=255, blank=True, null=True)
    process_id = models.TextField(blank=True, null=True, default=str(uuid.uuid4()))
    status = models.IntegerField(choices=STATUS_PROCESS, default=1)
    result = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.process_id
