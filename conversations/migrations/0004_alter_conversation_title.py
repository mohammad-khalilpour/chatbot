# Generated by Django 4.2.7 on 2023-11-16 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("conversations", "0003_alter_conversation_unique_together"),
    ]

    operations = [
        migrations.AlterField(
            model_name="conversation",
            name="title",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]