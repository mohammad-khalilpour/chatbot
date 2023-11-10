from django.db import models
import os


def chatbot_image_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"chatbot_{instance.user.id}.{ext}"

    return os.path.join('chatbot_images/', unique_filename)


class Chatbot(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500, blank=True)
    custom_prompt = models.TextField(blank=True)
    chatbot_picture = models.ImageField(blank=True, upload_to=chatbot_image_path)


class Content(models.Model):
    content = models.CharField(max_length=800)
    chatbot = models.ForeignKey(Chatbot, on_delete=models.CASCADE, related_name='contents')
