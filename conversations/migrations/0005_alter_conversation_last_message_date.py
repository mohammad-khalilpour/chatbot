# Generated by Django 4.2.7 on 2023-11-16 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("conversations", "0004_alter_conversation_title"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conversation",
            name="last_message_date",
            field=models.TimeField(auto_now=True),
        ),
    ]