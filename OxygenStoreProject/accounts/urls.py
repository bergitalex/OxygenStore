from django.urls import path
from .views import (UserRegisterView, CustomLoginView, CustomLogoutView, UserProfileView,
                    EditUsernameView, EditPasswordView, EditEmailView,
                    ConfirmEmailCodeView)
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('edit-username/', EditUsernameView.as_view(), name='edit-username'),
    path('edit-email/', EditEmailView.as_view(), name='edit-email'),
    path('edit-password/', EditPasswordView.as_view(), name='edit-password'),
    path('confirm-email/', ConfirmEmailCodeView.as_view(), name='confirm-email'),
]
