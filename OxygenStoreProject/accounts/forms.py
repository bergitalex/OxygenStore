from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from accounts.models import CustomUser


# Форма для регистрации пользователя
class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Подтвердите пароль')

    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

# Форма для изменения данных пользователя
class CustomUserChangeForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email')

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label=_("Email"), widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            UserModel = get_user_model()
            try:
                user = UserModel.objects.get(email=email)
                self.user_cache = authenticate(self.request, username=user.username, password=password)
                if self.user_cache is None:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )
            except UserModel.DoesNotExist:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )

        return self.cleaned_data


class ChangeNameForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username']
        labels = {
            'username': 'Имя пользователя'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите новое имя пользователя'})
        }


class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(label="Новый Email")

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(widget=forms.PasswordInput, label="Старый пароль")
    new_password = forms.CharField(widget=forms.PasswordInput, label="Новый пароль")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Подтвердите новый пароль")

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Пароли не совпадают.")