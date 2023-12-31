from django.shortcuts import render, redirect
from users.forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()


def register(request):
    if request.user.is_authenticated:
        return redirect('chat_list')

    register_form = RegistrationForm()

    if request.method == "POST":
        register_form = RegistrationForm(request.POST)

        if register_form.is_valid():
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password1']

            user = User.objects.create_user(email=email, password=password)
            user.set_password(password)
            user.save()
            return redirect('login')

    return render(request, 'register.html', {'form': register_form})


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request, data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            return redirect('chat_list')

    return render(request, 'login.html')

