from rest_framework.viewsets import ModelViewSet, GenericViewSet, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from posts.models import Thread, Message
from posts.serializers import ThreadSerializer, CreateThreadSerializer, CreateMessageSerializer, MessageSerializer
from posts.permissions import IsThreadParticipant, IsMessageSender, IsMessageReceiver, IsMessageParticipant

class ThreadViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateThreadSerializer
        
        if self.action == 'messages':
            return MessageSerializer
        
        return ThreadSerializer
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Thread.objects.all()
        return self.request.user.threads.all()
    
    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [IsAuthenticated()]
            
        return [IsAuthenticated(), IsThreadParticipant()]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        receiver = serializer.validated_data.pop('receiver')
        
        thread = Thread.objects \
            .filter(participants__in=[request.user]) \
            .filter(participants__in=[receiver])

        if thread.exists():
            thread = thread.first()
            serializer = self.get_serializer(instance=thread)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=200, headers=headers)
        
        serializer.save(participants=[request.user, receiver])
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=201, headers=headers)
    
    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        thread = self.get_object()
        paginator = LimitOffsetPagination()
        paginated_queryset = paginator.paginate_queryset(thread.messages.all(), request=request, view=self)
        return paginator.get_paginated_response(MessageSerializer(paginated_queryset, many=True).data)

class MessageViewSet(mixins.CreateModelMixin, GenericViewSet):
    def get_serializer_class(self):
        if self.action == 'create':
            return CreateMessageSerializer
        
        return MessageSerializer
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Message.objects.all()
        return Message.objects.filter(thread__participants__in=[self.request.user])

    def get_permissions(self):
        if self.action in ['create', 'list']:
            return [IsAuthenticated()]
        
        if self.action == 'mark_read':
            return [IsAuthenticated(), IsMessageReceiver()]
        

        return [IsAuthenticated(), IsMessageParticipant()]
    
    def perform_create(self, serializer):
        return serializer.save(sender=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def mark_read(self, request, pk=None):
        message = self.get_object()
        message.is_read = True
        message.save(update_fields=['is_read'])
        return Response(MessageSerializer(message).data)
    
    @action(detail=False, methods=['get'])
    def unread(self, request):
        unread_count = Message.objects.filter(thread__participants__in=[request.user], is_read=False).exclude(sender=request.user).count()
        return Response(
            {'unread_count': unread_count},
            200
        )
    
