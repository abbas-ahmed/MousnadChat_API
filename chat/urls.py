from django.urls import path
from . import views

urlpatterns = [
    path('chat_users/', views.get_chat_users, name='chat_users'),
    path('messages/', views.get_messages, name='get_messages'),
    path('send_message/', views.send_message, name='send_message'),
]