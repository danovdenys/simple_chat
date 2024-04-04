from django.db import models
from django.contrib.auth import get_user_model

from typing import Type, List, TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import User as UserModel

User = get_user_model()

class Message(models.Model):
    sender: "UserModel" = models.ForeignKey(to=User, on_delete=models.CASCADE)
    text = models.TextField()
    thread: "Thread" = models.ForeignKey(to='posts.Thread', on_delete=models.CASCADE, related_name='messages')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    @property
    def receiver(self) -> "UserModel":
        return self.thread.participants.exclude(pk=self.sender.pk).first()

class Thread(models.Model):
    participants = models.ManyToManyField(to=User, related_name='threads', related_query_name='thread', through='ThreadParticipant')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ThreadParticipant(models.Model):
    thread = models.ForeignKey(to=Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['thread', 'user'], name='unique_participant'),
        ]
        
