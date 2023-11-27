import json
import os
from django.core.management.base import BaseCommand
from chatbots.models import Chatbot, Content
from conversations.models import Message, Conversation
from users.models import User
from django.http import HttpRequest
from conversations.utils import most_related_document
from conversations.utils import get_embedding


class Command(BaseCommand):

    def handle(self, *args, **options):
        json_file_path = 'chatbots/management/data/data.jsonl'
        questions_embedding_file_path = 'chatbots/management/data/questions_embedding.jsonl'

        user = User.objects.filter(email='RagTest@gmail.com').first()
        if not user:
            user = User.objects.create_user('RagTest@gmail.com', 'RagTest@gmail.com', 'RagTest123456')

        chatbot = Chatbot.objects.filter(name='RagTest').first()
        if not chatbot:
            chatbot = Chatbot.objects.create(user=user, name='RagTest')

        conversation = Conversation.objects.filter(chatbot=chatbot, user=user).first()
        if not conversation:
            conversation = Conversation.objects.create(user=user, chatbot=chatbot)

        count = 0
        correct_count = 0
        with open(json_file_path, 'r', encoding='utf-8') as file:
            for i, line in enumerate(file):
                entry = json.loads(line)
                content = Content.objects.filter(content=entry['doc'], chatbot=chatbot).first()
                if not content:
                    Content.objects.create(chatbot=chatbot, content=entry['doc'], embedding=get_embedding(entry[doc]))
                self.stdout.write(self.style.SUCCESS(f'doc number {i} added successfully'))

            file.seek(0)

            questions = {}
            if os.path.isfile(questions_embedding_file_path):
                with open(questions_embedding_file_path, 'r', encoding='utf-8') as question_embedding_file:
                    for i, line in enumerate(question_embedding_file):
                        entry = json.loads(line)
                        questions[entry['question']] = entry['embedding']

            with open(questions_embedding_file_path, 'a', encoding='utf-8') as question_embedding_file:
                for i, line in enumerate(file):
                    entry = json.loads(line)
                    if entry['question'] not in questions:
                        questions_embedding = get_embedding(entry['question'])
                        question_embedding_file.write(
                            json.dumps({'question': entry['question'], 'embedding': questions_embedding}) + '\n'
                        )
                        questions[entry['question']] = questions_embedding

                    self.stdout.write(self.style.SUCCESS(f'question number {i} embedding saved successfully'))

            file.seek(0)
            for i, line in enumerate(file):
                entry = json.loads(line)
                question = entry['question']
                count += 1

                if most_related_document(conversation.id, question, questions.get(question)) == entry['doc']:
                    correct_count += 1
                    self.stdout.write(self.style.SUCCESS(f'doc number {i} retrieval succeeded'))
                else:
                    self.stdout.write(self.style.ERROR(f'doc number {i} retrieval failed'))
            print(f'success rate = {correct_count * 100 /count}%')

