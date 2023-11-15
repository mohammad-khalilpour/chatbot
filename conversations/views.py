from django.shortcuts import render
from conversations.models import Conversation
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
    context = {'chat_list': chat_list}
    return render(request, 'chat-list.html', context)
