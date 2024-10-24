from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.views.generic import ListView

from .models import Order, OrderItem
from .forms import OrderForm
from cart.models import CartItem
from products.models import Product

class CreateOrderView(LoginRequiredMixin, View):
    def get(self, request):
        form = OrderForm()
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price for item in cart_items)

        return render(request, 'orders/create_order.html', {
            'form': form,
            'cart_items': cart_items,
            'user_name': request.user.username,
            'user_email': request.user.email,
            'total_price': total_price,
        })

    @transaction.atomic
    def post(self, request):
        form = OrderForm(request.POST)
        cart_items = CartItem.objects.filter(user=request.user)

        if form.is_valid() and cart_items.exists():
            # Создаем заказ
            order = Order.objects.create(
                user=request.user,
                address=form.cleaned_data['address'],
                total_price=sum(item.total_price for item in cart_items)
            )

            # Переносим товары из корзины в OrderItem и уменьшаем их количество на складе
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

                # Уменьшаем количество товара на складе
                product = Product.objects.get(id=item.product.id)
                product.stock -= item.quantity
                product.save()

            # Очищаем корзину после оформления заказа
            cart_items.delete()

            return redirect('orders:order-success')

        return render(request, 'orders/create_order.html', {
            'form': form,
            'cart_items': cart_items,
            'user_name': request.user.username,
            'user_email': request.user.email,
            'total_price': sum(item.total_price for item in cart_items),
        })

class UserOrdersView(LoginRequiredMixin, View):
    def get(self, request):
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        return render(request, 'orders/my_orders.html', {'orders': orders})


class MyOrdersView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items__product')

class CancelOrderView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        order.delete()
        return redirect('orders:my-orders')