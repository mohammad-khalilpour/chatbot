from django.shortcuts import render, redirect
from users.forms import RegistrationForm


def register(request):
    register_form = RegistrationForm()

    if request.method == "POST":
        register_form = RegistrationForm(request.POST)

        if register_form.is_valid():
            user = register_form.save()
            user.set_password(user.password)
            user.save()

    return render(request, 'register.html', {'form': register_form})
