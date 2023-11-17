# Generated by Django 4.2.7 on 2023-11-17 13:40

import chatbots.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatbots", "0003_alter_chatbot_chatbot_picture"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chatbot",
            name="chatbot_picture",
            field=models.ImageField(
                blank=True, upload_to=chatbots.models.chatbot_image_path
            ),
        ),
    ]