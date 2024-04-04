from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from core.serializers import UserSerializer, CreateUserSerializer, LoginSerializer

User = get_user_model()

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateUserSerializer
        
        if self.action == 'login':
            return LoginSerializer
        return UserSerializer
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        return Response(UserSerializer(request.user).data, status=200)
    
    @action(detail=False, methods=['post'])
    def logout(self, request):
        Token.objects.filter(user=request.user).delete()
        return Response({}, status=204)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(username=serializer.validated_data['username'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': dict(UserSerializer(user).data)})
    
