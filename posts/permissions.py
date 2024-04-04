from rest_framework.permissions import BasePermission
from posts.models import Thread, Message, User


class IsThreadParticipant(BasePermission):
    def has_object_permission(self, request, view, obj: "Thread"):
        return obj.participants.filter(pk=request.user.pk).exists()

class IsMessageSender(BasePermission):
    def has_object_permission(self, request, view, obj: "Message"):
        return obj.sender.pk == request.user.pk

class IsMessageReceiver(BasePermission):
    def has_object_permission(self, request, view, obj: "Message"):
        return request.user.pk == obj.receiver.pk
    
class IsMessageParticipant(BasePermission):
    def has_object_permission(self, request, view, obj: "Message"):
        return obj.thread.participants.filter(pk=request.user.pk).exists()