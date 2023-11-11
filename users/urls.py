from django.urls import path
from users.views import register

urlpatterns = [
    path("register/", register, name='register'),
]