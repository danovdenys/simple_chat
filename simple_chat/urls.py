from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

api_urlpatterns = [
    path('posts/', include('posts.urls')),
    path('core/', include('core.urls')),
    # YOUR PATTERNS
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/', include(api_urlpatterns)),
]
