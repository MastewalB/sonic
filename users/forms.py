from django import forms
from django.contrib.auth.forms import AuthenticationForm
from users.models import User


class AdminLoginForm(AuthenticationForm):
    # def __init__(self, *args, **kwargs):
    #     super(AdminLoginForm, self).__init__(*args, **kwargs)

    username = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')

    # def __init__(self, request, *args, **kwargs):
    #     super(AdminLoginForm, self).__init__(*args, **kwargs)

    # class Meta:
    #     model = User
    #     fields = ('email', 'password')
