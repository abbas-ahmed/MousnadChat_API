from django.db import models
from django.contrib.auth.models import User
import os
import uuid
from datetime import datetime

def voice_upload_path(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4()}.{ext}"
    now = datetime.now()
    return os.path.join(
        'voice_messages',
        str(instance.sender.id),
        str(now.year),
        str(now.month),
        new_filename
    )



class Message(models.Model):
    sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
    content = models.TextField()
    voice = models.FileField(upload_to=voice_upload_path, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:50]}"
