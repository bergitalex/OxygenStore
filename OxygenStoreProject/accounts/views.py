from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy, reverse

from .emailchecker import generate_confirmation_code, send_confirmation_email
from .forms import (CustomUserCreationForm, EmailAuthenticationForm,
                    ChangeNameForm, ChangeEmailForm, ChangePasswordForm)

# Представление для регистрации пользователя
class UserRegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('core:main-page')  # Перенаправление на главную страницу после успешной регистрации
        else:
            return render(request, 'registration/register.html', {'form': form})

# Кастомное представление для входа пользователя
class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        remember_me = self.request.POST.get('remember_me')
        if not remember_me:
            # Установить сессию без сохранения, чтобы она завершилась после закрытия браузера
            self.request.session.set_expiry(6000)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('core:main-page')

    def form_invalid(self, form):
        messages.error(self.request, "Неправильное имя пользователя или пароль. Попробуйте еще раз.")
        return super().form_invalid(form)

# Представление для выхода пользователя
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Вы успешно вышли из системы.")
        return redirect('accounts:login')

# Представление профиля пользователя
class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/profile.html'

# Представление для изменения имени
class EditUsernameView(LoginRequiredMixin, FormView):
    template_name = 'accounts/change_name.html'
    form_class = ChangeNameForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        user = self.request.user
        user.username = form.cleaned_data['username']  # Используем только 'username'
        user.save()
        messages.success(self.request, "Имя пользователя успешно изменено.")
        return super().form_valid(form)

# Представление для изменения email с подтверждением
class EditEmailView(LoginRequiredMixin, FormView):
    template_name = 'accounts/change_email.html'
    form_class = ChangeEmailForm
    success_url = reverse_lazy('accounts:confirm-email')

    def form_valid(self, form):
        new_email = form.cleaned_data['new_email']
        # Генерация и отправка кода подтверждения
        confirmation_code = generate_confirmation_code()
        send_confirmation_email(new_email, confirmation_code)

        # Сохранение кода и email в сессии для последующего подтверждения
        self.request.session['confirmation_code'] = confirmation_code
        self.request.session['new_email'] = new_email

        return super().form_valid(form)

# Подтверждение изменения email через код
class ConfirmEmailCodeView(LoginRequiredMixin, View):
    template_name = 'accounts/change_email_code.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        confirmation_code = request.POST.get('confirmation_code')
        session_code = request.session.get('confirmation_code')
        new_email = request.session.get('new_email')

        if confirmation_code == session_code and new_email:
            user = request.user
            user.email = new_email
            user.save()
            # Очистка данных сессии
            del request.session['confirmation_code']
            del request.session['new_email']
            messages.success(request, "Email успешно изменен.")
            return redirect('accounts:profile')
        else:
            messages.error(request, "Неверный код подтверждения.")
            return redirect('accounts:confirm-email')

# Представление для изменения пароля
class EditPasswordView(LoginRequiredMixin, FormView):
    template_name = 'accounts/change_password.html'
    form_class = ChangePasswordForm
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        user = self.request.user
        old_password = form.cleaned_data['old_password']
        if not user.check_password(old_password):
            form.add_error('old_password', 'Неверный старый пароль.')
            return self.form_invalid(form)

        user.set_password(form.cleaned_data['new_password'])
        user.save()
        update_session_auth_hash(self.request, user)  # Обновление сессии для пользователя
        messages.success(self.request, "Пароль успешно изменен.")
        return super().form_valid(form)
