from django.contrib import admin
from django.urls import path
from conversations.views import chat_list_view, create_chat_view

urlpatterns = [
    path('', chat_list_view, name="chat_list"),
    path('create/', create_chat_view, name="create_chat"),
]