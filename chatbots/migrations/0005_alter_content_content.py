# Generated by Django 4.2.7 on 2023-11-21 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chatbots", "0004_alter_content_embedding"),
    ]

    operations = [
        migrations.AlterField(
            model_name="content",
            name="content",
            field=models.TextField(max_length=800),
        ),
    ]