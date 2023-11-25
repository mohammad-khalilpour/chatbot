from openai import OpenAI
from conversations.models import Conversation, Message
from chatbots.models import Chatbot, Content
from django.conf import settings
import json
from pgvector.django import L2Distance


def open_ai_api_chat_completion(conversation_id, reproduce=False):
    conversation = Conversation.objects.get(id=conversation_id)
    client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url='https://openai.torob.ir/v1')
    if reproduce:
        Message.objects.filter(conversation=conversation).last().delete()
    messages = Message.objects.filter(conversation=conversation)
    if not conversation.title:
        title = client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=10,
            messages=[
                {'role': 'system', 'content': 'Create a title for the following message'},
                {'role': 'user', 'content': messages[0].message_context}
            ]
        )
        title = json.loads(title) if isinstance(title, str) else json.loads(title.model_dump_json())
        conversation.title = title['choices'][0]['message']['content']
        conversation.save()
    related_document = most_related_document(conversation_id, messages.last().message_context)
    req_messages = [{"role": "system", "content": conversation.chatbot.custom_prompt},]
    for message in messages:
        if message.is_chatbot_message:
            role = 'assistant'
        else:
            role = 'user'

        req_messages.append({'role': role, 'content': message.message_context})
    req_messages.append({"role": "system", "content": f"if there is any data about the next question then answer based on ${related_document}"})
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=req_messages
    )
    completion = json.loads(completion) if isinstance(completion, str) else json.loads(completion.model_dump_json())
    Message.objects.create(conversation=conversation, message_context=completion['choices'][0]['message']['content'],
                           is_chatbot_message=True).save()
    conversation.update_datetime_field_to_now()


def most_related_document(conversation_id, message):
    client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url='https://openai.torob.ir/v1')
    response = client.embeddings.create(
        input=message,
        model='text-embedding-ada-002',
        encoding_format='float'
    )
    response = json.loads(response) if isinstance(response, str) else json.loads(response.model_dump_json())
    message_embedding = response['data'][0]['embedding']
    conversation = Conversation.objects.get(id=conversation_id)
    chatbot = conversation.chatbot
    most_related_doc = Content.objects.filter(chatbot=chatbot).order_by(L2Distance('embedding', message_embedding))[0]
    return most_related_doc.content
