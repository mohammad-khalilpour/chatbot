import json
from django.core.management.base import BaseCommand
from chatbots.models import Chatbot, Content
from conversations.models import Message, Conversation
from users.models import User
from chatbots.admin import ContentAdmin
from django.contrib import admin
from django.http import HttpRequest
from conversations.utils import most_related_document


class Command(BaseCommand):

    def handle(self, *args, **options):
        json_file_path = 'chatbots/management/data/data.jsonl'

        user = User.objects.filter(email='RagTest@gmail.com').first()
        if not user:
            user = User.objects.create_user('RagTest@gmail.com', 'RagTest@gmail.com', 'RagTest123456')

        chatbot = Chatbot.objects.filter(name='RagTest').first()
        if not chatbot:
            chatbot = Chatbot.objects.create(user=user, name='RagTest')

        conversation = Conversation.objects.filter(chatbot=chatbot, user=user).first()
        if not conversation:
            conversation = Conversation.objects.create(user=user,chatbot=chatbot)

        count = 0
        correct_count = 0
        with open(json_file_path, 'r', encoding='utf-8') as file:

            for i, line in enumerate(file):
                entry = json.loads(line)
                content = Content.objects.filter(content=entry['doc'], chatbot=chatbot).first()
                if not content:
                    content = Content(
                        chatbot=chatbot,
                        content=entry['doc']
                    )
                    request = HttpRequest()
                    request.method = 'POST'
                    request.POST = {'content': entry['doc']}
                    ContentAdmin(Content, admin.site).save_model(request, content, None, False)
                self.stdout.write(self.style.SUCCESS(f'doc number {i} added successfully'))

            file.seek(0)

            for i, line in enumerate(file):
                entry = json.loads(line)
                question = entry['question']
                count += 1

                if most_related_document(conversation.id, question) == entry['doc']:
                    correct_count += 1
                    self.stdout.write(self.style.SUCCESS(f'doc number {i} retrieval succeeded'))
                else:
                    self.stdout.write(self.style.ERROR(f'doc number {i} retrieval failed'))
            print(f'success rate = {correct_count * 100 /count}%')

