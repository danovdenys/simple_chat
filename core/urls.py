from django.urls import path
from rest_framework.routers import DefaultRouter

from core.viewsets import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, 'user')


urlpatterns = [] + router.urls