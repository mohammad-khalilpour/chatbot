from django.shortcuts import render
from conversations.models import Conversation, Message
from chatbots.models import Chatbot
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger


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


def chat_detail_view(request):
    conversation_id = request.GET.get('conversation')
    conversation = Conversation.objects.get(id=conversation_id)

    if request.method == 'POST':
        message_context = request.POST.get('message')
        Message.objects.create(conversation=conversation, message_context=message_context,is_chatbot_message=False).save()

    messages = Message.objects.filter(conversation=conversation)
    context = {'conversation_id': conversation_id, 'messages': messages}

    return render(request, 'chat-details.html', context)
