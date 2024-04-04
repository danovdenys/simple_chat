from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from posts.models import Thread, Message, User
from posts.serializers import ThreadSerializer, MessageSerializer
from posts.viewsets import ThreadViewSet, MessageViewSet
from rest_framework.authtoken.models import Token

class ThreadViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

        self.sender = User.objects.create(username='sender', password='senderpassword')
        self.token = Token.objects.create(user=self.sender)
        self.receiver = User.objects.create(username='receiver', password='receiverpassword')

        self.thread = Thread.objects.create()
        self.thread.participants.add(self.sender, self.receiver)
        Message.objects.create(thread=self.thread, sender=self.sender, text='Test Message')
        self.viewset = ThreadViewSet.as_view({'get': 'list', 'post': 'create'})
        self.detail_viewset = ThreadViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'})
        self.message_viewset = ThreadViewSet.as_view({'get': 'messages'})

    def test_create_duplicate_thread(self):
        request = self.factory.post(
            '/api/posts/threads/', 
            {'receiver': self.receiver.id},
            format='json', 
            headers={'Authorization': f'Token {self.token.key}'})
        
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK) # It should return existing thread if it exists

    def test_create_thread(self):
        new_receiver = User.objects.create(username='new_receiver', password='new_receiver_password')
        request = self.factory.post(
            '/api/posts/threads/', 
            {'receiver': new_receiver.id}, 
            format='json', 
            headers={'Authorization': f'Token {self.token.key}'})
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_list_threads(self):
        request = self.factory.get(
            '/api/posts/threads/', 
            format='json', 
            headers = {'Authorization': f'Token {self.token.key}'})
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
    
    def test_list_messages(self):
        request = self.factory.get(
            f'/api/posts/threads/{self.thread.pk}/messages/',
            format='json',
            headers = {'Authorization': f'Token {self.token.key}'})
        response = self.message_viewset(request, pk=self.thread.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)



class MessageViewSetTestCase(APITestCase):
    def setUp(self):
        self.client = APIRequestFactory()
        self.sender = User.objects.create(username='sender', password='senderpassword')
        self.sender_token = Token.objects.create(user=self.sender)
        self.receiver = User.objects.create(username='receiver', password='receiverpassword')
        self.receiver_token = Token.objects.create(user=self.receiver)
        self.thread = Thread.objects.create()
        self.thread.participants.add(self.sender, self.receiver)
        self.message = Message.objects.create(thread=self.thread, sender=self.sender, text='Test Message')
        self.viewset = MessageViewSet.as_view({'post': 'create'})
        self.detail_viewset = MessageViewSet.as_view({'patch': 'mark_read'})
        self.unread_viewset = MessageViewSet.as_view({'get': 'unread'})
    
    def test_create_message(self):
        request = self.client.post(
            '/api/posts/messages/', 
            {'text': 'Test Message', 'thread': self.thread.id},
            format='json', 
            headers={'Authorization': f'Token {self.sender_token.key}'})
        response = self.viewset(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_mark_read(self):
        request = self.client.patch(
            f'/api/posts/messages/{self.message.pk}/mark_read/',
            format='json',
            headers = {'Authorization': f'Token {self.receiver_token.key}'})
        response = self.detail_viewset(request, pk=self.message.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_read'])
    
    def test_unread(self):
        request = self.client.get(
            '/api/posts/messages/unread/',
            format='json',
            headers = {'Authorization': f'Token {self.receiver_token.key}'})
        response = self.unread_viewset(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['unread_count'] > 0)