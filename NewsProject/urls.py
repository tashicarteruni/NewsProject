"""NewsProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from NewsApp.views import (
    login_view, logout_view, check_status, post_story, get_stories, delete_stories
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login', login_view, name='login'),
    path('api/logout', logout_view, name='logout'),
    path('api/check_status', check_status, name='check_status'),
    path('api/stories', post_story, name='post_story'),  # Changed URL for posting a story
    path('api/stories', get_stories, name='get_stories'),  # Changed URL for getting stories
    path('api/stories/<str:key>', delete_stories, name='delete_stories'),
]
