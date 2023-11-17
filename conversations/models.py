from django.db import models
from users.models import User
from chatbots.models import Chatbot
from datetime import datetime


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, blank=True)
    last_message_date = models.DateTimeField(auto_now=True)
    like_count = models.BigIntegerField(default=0)
    dislike_count = models.BigIntegerField(default=0)

    class Meta:
        ordering = ['-last_message_date']

    def update_datetime_field_to_now(self):
        self.last_message_date = datetime.now()
        self.save()


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    is_chatbot_message = models.BooleanField()
    message_context = models.TextField()
    date = models.DateTimeField(auto_now=True)
    like = models.BooleanField(null=True, default=None)

    class Meta:
        ordering = ['date']
