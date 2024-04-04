from django.urls import path

from rest_framework.routers import DefaultRouter

from posts.viewsets import ThreadViewSet, MessageViewSet

router = DefaultRouter()
router.register('threads', ThreadViewSet, 'thread')
router.register('messages', MessageViewSet, 'message')

urlpatterns = router.urls
