from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from conversations.models import Conversation, Message
from chatbots.models import Chatbot, Content


CHATLIST_URL = reverse('chat_list')


def create_user(email='example@123.com', password='test1234'):
    return get_user_model().objects.create_user(email=email, password=password)


class ChatListView(TestCase):
    def setUp(self):
        self.user = create_user()
        chatbot_user = create_user(email='ChatbotUser@gmail.com')
        self.chatbot = Chatbot.objects.create(name='gpt', user=chatbot_user)
        self.conversation1 = Conversation.objects.create(user=self.user, chatbot=self.chatbot)
        self.conversation2 = Conversation.objects.create(user=self.user, chatbot=self.chatbot)
        self.conversation3 = Conversation.objects.create(user=chatbot_user, chatbot=self.chatbot)

    def test_successful_chat_list(self):
        self.client.force_login(self.user)
        res = self.client.get(CHATLIST_URL)

        self.assertEqual(res.status_code, 200)
        chat_list = Conversation.objects.filter(user=self.user)
        self.assertQuerysetEqual(res.context['chat_list'], chat_list)

    def test_unauthorized_login(self):
        res = self.client.get(CHATLIST_URL)

        self.assertEqual(res.status_code, 302)
        self.assertNotIn('context', res)
