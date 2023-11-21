from django.db import models
from django.conf import settings
from pgvector.django import VectorField
import os


def chatbot_image_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"chatbot_{instance.user.id}.{ext}"

    return os.path.join('chatbot_images/', unique_filename)


class Chatbot(models.Model):
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    description = models.TextField(blank=True)
    custom_prompt = models.TextField(blank=True)
    chatbot_picture = models.ImageField(blank=True, upload_to=chatbot_image_path)
    is_disabled = models.BooleanField(default=False)
    like_count = models.BigIntegerField(default=0)
    dislike_count = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name


class Content(models.Model):
    content = models.CharField(max_length=800)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE, related_name='contents')
    embedding = VectorField(dimensions=1536, blank=True, null=True)
