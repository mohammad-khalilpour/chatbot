from django.db import models
from users.models import User
from chatbots.models import Chatbot


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    last_message_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_message_date']


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    is_chatbot_message = models.BooleanField()
    message_context = models.TextField()
    like = models.BooleanField(null=True, default=None)
