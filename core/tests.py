from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.routers import DefaultRouter
from core.viewsets import UserViewSet

User = get_user_model()

class UserViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.viewset = UserViewSet.as_view({'get': 'list', 'post': 'create'})
        self.login_viewset = UserViewSet.as_view({'post': 'login'})
        self.logout_viewset = UserViewSet.as_view({'post': 'logout'})
        self.me_viewset = UserViewSet.as_view({'get': 'me'})
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

    def test_list_users(self):
        request = self.factory.get('/api/core/users/', format='json')
        response = self.viewset(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data) > 0)

    def test_create_user(self):
        request = self.factory.post('/api/core/users/', {'username': 'newuser', 'password': 'newpassword'}, format='json')
        response = self.viewset(request)
        self.assertEqual(response.status_code, 201) 
        self.assertTrue(len(response.data) > 0)

    def test_get_current_user(self):
        request = self.factory.get('/api/core/users/me/', format='json', headers={'Authorization': f'Token {self.token.key}'})
        request.user = self.user
        response = self.me_viewset(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['username'], self.user.username)

    def test_logout_user(self):
        request = self.factory.post('/api/core/users/logout/', format='json', headers={'Authorization': f'Token {self.token.key}'})
        request.user = self.user
        response = self.logout_viewset(request)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Token.objects.filter(user=self.user).exists())

    def test_login_user(self):
        request = self.factory.post('/api/core/users/login/', {'username': 'testuser', 'password': 'testpassword'}, format='json')
        response = self.login_viewset(request)
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.data)
        self.assertIn('user', response.data)
        self.assertEqual(response.data['user']['username'], self.user.username)

