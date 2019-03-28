import datetime
from django.contrib.auth.hashers import check_password
from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as __


from .models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text=__('Required'))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    # TODO EXPAND VALIDATION WITH 5 ATTEMPT BLOCK AND DISPLAY INFO (RECOVER PASSWORD AFTER FIRST ATTEMPT)
    # def clean(self):
        # IF YOU WANT TO CLEAN IN GENERAL AND ADD CUSTOM MSG TO ONE FIELD, USE self.add_error(field_name, msg)

    def clean_username(self):
        username = self.cleaned_data.get('username')

        exists = User.objects.filter(username=username).exists()
        if exists:
            raise ValidationError(__('HE EXISTS'))
        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError(__("Password don't match"))

        return password1

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data.get('username'),
            email=self.cleaned_data.get('email'),
            password=self.cleaned_data.get('password1')
        )
        return user


class LogInForm(forms.Form):
    username = forms.CharField(label='Enter your username')
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise ValidationError(__('qwe provided incorrect data'))

        auth = check_password(password, user.password)
        if not auth:
            raise ValidationError(__('qwe provided incorrect data'))
        return password

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(request, username=username, password=password)
        return user


class ChangePasswordForm(PasswordChangeForm):
    pass


