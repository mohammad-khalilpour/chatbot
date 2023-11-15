from django.contrib import admin
from chatbots.models import Chatbot, Content
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(Chatbot)
class ChatbotAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def get_queryset(self, request):
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

    def get_queryset(self, request):
        chatbot_list = Chatbot.objects.all().filter(user=request.user)
        return Content.objects.all().filter(chatbot__in=chatbot_list)

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['chatbot'].queryset = Chatbot.objects.filter(user=request.user)
        return form

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

