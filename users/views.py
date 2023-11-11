from django.shortcuts import render, redirect
from users.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()


def register(request):
    register_form = RegistrationForm()

    if request.method == "POST":
        register_form = RegistrationForm(request.POST)

        if register_form.is_valid():
            user = User(register_form.save())
            user.set_password(user.password)
            user.create()

    return render(request, 'register.html', {'form': register_form})


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request, data=request.POST)

        if login_form.is_valid():
            return redirect('https://torob.com/')

    return render(request, 'login.html')

