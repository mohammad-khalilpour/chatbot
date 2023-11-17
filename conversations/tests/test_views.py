from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from conversations.models import Conversation, Message
from chatbots.models import Chatbot, Content


CHATLIST_URL = reverse('chat_list')
CREATE_CHAT_URL = reverse('create_chat')
CHAT_DETAIL_URL = reverse('chat_detail')


def create_user(email='example@123.com', password='test1234'):
    return get_user_model().objects.create_user(email=email, password=password)


class ChatListViewTEST(TestCase):
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


class CreateChatViewTest(TestCase):
    def setUp(self):
        self.user = create_user()
        chatbot_user = create_user(email='ChatbotUser@gmail.com')
        self.chatbot1 = Chatbot.objects.create(name='gpt', user=chatbot_user)
        self.chatbot2 = Chatbot.objects.create(name='anotherGpt', user=chatbot_user)

    def test_successful_create_chat_view(self):
        self.client.force_login(self.user)
        res = self.client.get(CREATE_CHAT_URL)

        self.assertEqual(res.status_code, 200)
        chatbots = Chatbot.objects.all()
        self.assertSetEqual(res.context['chatbot_list'], chatbots)

    def test_unauthorized_login(self):
        res = self.client.get(CREATE_CHAT_URL)

        self.assertEqual(res.status_code, 302)
        self.assertNotIn('context', res)


class ChatDetailViewTest(TestCase):
    def setUp(self):
        self.user = create_user()
        chatbot_user = create_user(email='ChatbotUser@gmail.com')
        self.chatbot = Chatbot.objects.create(name='gpt', user=chatbot_user)
        self.conversation = Conversation.objects.create(user=self.user, chatbot=self.chatbot)
        self.message1 = Message(conversation=self.conversation, is_chatbot_message=0, message_context="some test")
        self.message2 = Message(conversation=self.conversation, is_chatbot_message=1, message_context="some answer")
        self.message3 = Message(conversation=self.conversation, is_chatbot_message=0, message_context="another test")
        self.message4 = Message(conversation=self.conversation, is_chatbot_message=2, message_context="another answer")

    def test_successful_chat_detail(self):
        self.client.force_login(self.user)
        res = self.client.get(CHAT_DETAIL_URL + f'?conversation={self.conversation.id}')

        self.assertEqual(res.status_code, 200)
        messages = Message.objects.filter(conversation=self.conversation)
        self.assertQuerysetEqual(res.context['messages'], messages)

    def test_unauthorized_login(self):
        res = self.client.get(CHAT_DETAIL_URL)

        self.assertEqual(res.status_code, 302)
        self.assertNotIn('context', res)
