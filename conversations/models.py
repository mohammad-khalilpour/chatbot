from django.db import models
from users.models import User
from chatbots.models import Chatbot


class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'chatbot')
