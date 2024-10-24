from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import MainView, CategoryProductsView

app_name = 'core'

urlpatterns = [
    path('', MainView.as_view(), name='main-page'),
    path('category/<int:pk>/', CategoryProductsView.as_view(), name='category-products'),
]