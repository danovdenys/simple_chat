from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from posts.models import Thread, Message, User


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['pk', 'sender', 'text', 'thread_id', 'created_at', 'is_read']

class CreateMessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = ['text', 'thread']

class CreateThreadSerializer(ModelSerializer):
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)

    class Meta:
        model = Thread
        fields = ['receiver', 'pk', 'participants', 'created_at', 'updated_at', 'messages']
        extra_kwargs = {
            'participants': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'messages': {'read_only': True},
        }

    
    def validate_receiver(self, value):
        if value == self.context['request'].user:
            raise serializers.ValidationError('You cannot send a message to yourself.')
        return value
    
    def is_valid(self, *, raise_exception=False):
        return super().is_valid(raise_exception=raise_exception)

class ThreadSerializer(ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    class Meta:
        model = Thread
        fields = ['pk', 'participants', 'created_at', 'updated_at', 'messages']
    
    