"""
URL configuration for Chatting_System project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from ChatApp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage),
    path('about/', views.aboutpage),
    path('register/', views.register),
    path('login/', views.login),
    path('verify/', views.auth_verify),
    path('logout/', views.logout),
    path('contactus/', views.contactus),
    path('recovery/', views.pw_recovery),
    path('users/', views.user_lists),
    path('start_chat/<int:phoneno>/', views.start_chat, name='start_chat'),
    path('chat/', views.chat, name='chat'),
    path('history/', views.history),
    path('change-password/', views.update_password),
    path('change-picture/', views.change_pic),
    path('2fa/', views.reg_auth),
    path('delete-auth/', views.delete_auth),
    path('turnoff-auth/', views.turnoff_auth),
]
