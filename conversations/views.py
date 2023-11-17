from django.shortcuts import render
from conversations.models import Conversation, Message
from chatbots.models import Chatbot
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger
from openai import OpenAI
from django.conf import settings
import json


@login_required
def chat_list_view(request):
    items_per_page = 10

    queryset = Conversation.objects.filter(user=request.user)

    paginator = Paginator(queryset, items_per_page)
    page = request.GET.get('page')

    try:
        chat_list = paginator.page(page)
    except PageNotAnInteger:
        chat_list = paginator.page(1)
    context = {'chat_list': chat_list, 'page_count': range(1, int((queryset.count() - 1) / 10) + 2)}
    return render(request, 'chat-list.html', context)


@login_required
def create_chat_view(request):
    chatbots = Chatbot.objects.all()

    context = {'chatbot_list': chatbots}

    if request.method == 'POST':
        chatbot_name = request.POST.get('chatbot_name')
        chatbot = Chatbot.objects.get(name=chatbot_name)
        Conversation.objects.create(chatbot=chatbot, user=request.user, title='').save()

    return render(request, 'create-chat.html', context)


@login_required
def chat_detail_view(request):
    conversation_id = request.GET.get('conversation')
    conversation = Conversation.objects.get(id=conversation_id)

    if request.method == 'POST':
        react = request.POST.get('react')
        if react:
            message = Message.objects.filter(conversation=conversation).last()
            if react == 'like':
                message.like = True
                message.save()
                conversation.like_count += 1
                conversation.save()
            elif react == 'dislike':
                message.like = False
                message.save()
                open_ai_api_chat_completion(conversation_id, reproduce=True)
                conversation.dislike_count += 1
                conversation.save()

        else:
            message_context = request.POST.get('message')
            Message.objects.create(conversation=conversation, message_context=message_context, is_chatbot_message=False).save()
            open_ai_api_chat_completion(conversation_id)

    messages = Message.objects.filter(conversation=conversation)
    context = {'conversation_id': conversation_id, 'messages': messages}

    return render(request, 'chat-details.html', context)


def open_ai_api_chat_completion(conversation_id, reproduce=False):
    conversation = Conversation.objects.get(id=conversation_id)
    client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url='https://openai.torob.ir/v1')
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
        title = json.loads(title)
        conversation.title = title['choices'][0]['message']['content']
        conversation.save()
    req_messages = [{"role": "system", "content": conversation.chatbot.custom_prompt}, ]
    for message in messages:
        if message.is_chatbot_message:
            role = 'assistant'
        else:
            role = 'user'

        req_messages.append({'role': role, 'content': message.message_context})
    if reproduce:
        req_messages.pop()
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=req_messages
    )
    completion = json.loads(completion)
    if reproduce:
        Message.objects.filter(conversation=conversation).last().delete()
    Message.objects.create(conversation=conversation, message_context=completion['choices'][0]['message']['content'],
                           is_chatbot_message=True).save()
    conversation.update_datetime_field_to_now()
