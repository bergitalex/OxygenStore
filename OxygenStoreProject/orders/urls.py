from django.urls import path
from django.views.generic import TemplateView

from .views import CreateOrderView, UserOrdersView

app_name = 'orders'

urlpatterns = [
    path('create/', CreateOrderView.as_view(), name='create-order'),
    path('my-orders/', UserOrdersView.as_view(), name='my-orders'),
    path('order-success/', TemplateView.as_view(template_name="orders/order_success.html"), name='order-success'),
    path('cancel-order/<int:pk>/', CreateOrderView.as_view(), name='cancel-order'),
]
