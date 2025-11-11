"""
URL configuration for myproject project.
"""
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin-panal/', admin.site.urls),
    path('api/', include('codegraphers.urls')),        # SQL routes
    path('api/', include('codegraphers.urls_mongo')),  # MongoDB routes
    path('api-auth/', include('rest_framework.urls')),
]