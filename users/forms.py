from django import forms
from django.contrib.auth.forms import BaseUserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegistrationForm(BaseUserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password2'}))

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
