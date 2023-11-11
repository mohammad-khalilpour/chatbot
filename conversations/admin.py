from django.contrib import admin
from conversations.models import Conversation, Message

admin.site.register(Conversation)
admin.site.register(Message)
