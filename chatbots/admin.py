from django.contrib import admin
from chatbots.models import Chatbot, Content
from django.contrib.auth import get_user_model
from openai import OpenAI
from django.conf import settings
import json

User = get_user_model()


@admin.register(Chatbot)
class ChatbotAdmin(admin.ModelAdmin):
    list_display = ('name',)
    readonly_fields = ['like_count', 'dislike_count']

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super().get_queryset(request)
        elif request.user.is_chatbot_creator:
            return Chatbot.objects.all().filter(user=request.user)

    def get_form(self, request, obj=None, change=False, **kwargs):
        self.exclude = ('user',)
        form = super().get_form(request, obj, **kwargs)
        return form

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        is_superuser = request.user.is_superuser
        is_chatbot_creator = request.user.is_chatbot_creator
        if is_superuser or is_chatbot_creator:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        is_superuser = request.user.is_superuser
        is_chatbot_creator = request.user.is_chatbot_creator
        if is_superuser or (is_chatbot_creator and obj and obj.user == request.user):
            return True
        return False


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ('content',)
    readonly_fields = ('embedding', )

    def get_queryset(self, request):
        chatbot_list = []
        if request.user.is_superuser:
            chatbot_list = Chatbot.objects.all()
        elif request.user.is_chatbot_creator:
            chatbot_list = Chatbot.objects.all().filter(user=request.user)
        return Content.objects.all().filter(chatbot__in=chatbot_list)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if request.user.is_chatbot_creator:
            form.base_fields['chatbot'].queryset = Chatbot.objects.filter(user=request.user)
        return form

    def save_model(self, request, obj, form, change):
        client = OpenAI(api_key=settings.OPENAI_API_KEY, base_url='https://openai.torob.ir/v1')
        response = client.embeddings.create(
            input=request.POST.get('content'),
            model='text-embedding-ada-002',
            encoding_format='float'
        )
        response = json.loads(response) if isinstance(response, str) else json.loads(response.model_dump_json())
        obj.embedding = response['data'][0]['embedding']
        super().save_model(request, obj, form, change)

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        is_superuser = request.user.is_superuser
        is_chatbot_creator = request.user.is_chatbot_creator
        if is_superuser or is_chatbot_creator:
            return True
        return False

    def has_change_permission(self, request, obj=None):
        is_superuser = request.user.is_superuser
        is_chatbot_creator = request.user.is_chatbot_creator
        if is_superuser or (is_chatbot_creator and obj and obj.chatbot.user == request.user):
            return True
        return False

