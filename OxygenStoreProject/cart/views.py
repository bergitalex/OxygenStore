import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import View, TemplateView
from products.models import Product
from .models import CartItem

class AddToCartView(View):
    def post(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        quantity = 1
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Требуется авторизация'}, status=403)

        if product.stock < quantity:
            return JsonResponse({'status': 'error', 'message': 'Недостаточно товара на складе'}, status=400)

        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            new_quantity = cart_item.quantity + quantity
            if new_quantity > product.stock:
                return JsonResponse({'status': 'error', 'message': 'Недостаточно товара на складе'}, status=400)
            cart_item.quantity = new_quantity
        else:
            cart_item.quantity = quantity

        cart_item.save()
        return JsonResponse({'status': 'success', 'message': 'Товар добавлен в корзину'}, status=200)


class UpdateCartItemQuantityView(View):
    def post(self, request, product_id):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'message': 'Требуется авторизация'}, status=403)

        # Получаем новое количество товара из тела запроса
        data = json.loads(request.body)
        new_quantity = int(data.get('quantity', 0))

        # Получаем товар и проверяем наличие на складе
        product = Product.objects.get(id=product_id)
        if new_quantity > product.stock:
            return JsonResponse({'status': 'error', 'message': f'На складе доступно максимум {product.stock} единиц'}, status=400)

        # Обновляем количество товара в корзине
        cart_item = CartItem.objects.filter(user=request.user, product=product).first()
        if cart_item:
            if new_quantity <= product.stock:
                cart_item.quantity = new_quantity
                cart_item.save()
            else:
                return JsonResponse({'status': 'error', 'message': 'Товар не найден в корзине'}, status=404)
            return JsonResponse({'status': 'success', 'message': 'Количество обновлено'}, status=200)
        return JsonResponse({'status': 'error', 'message': 'Товар не найден в корзине'}, status=404)

class CheckCartItemsView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'cart_items': []}, status=200)

        cart_items = CartItem.objects.filter(user=request.user)
        items_data = [
            {'product_id': item.product.id, 'quantity': item.quantity} for item in cart_items
        ]

        return JsonResponse({'cart_items': items_data}, status=200)

class CartDetailView(TemplateView):
    template_name = 'cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=self.request.user).order_by('product__name')
            context['cart_items'] = cart_items
            context['total_price'] = sum(item.total_price for item in cart_items)
        else:
            cart = self.request.session.get('cart', {})
            context['cart_items'] = cart.values()
            context['total_price'] = sum(item['price'] * item['quantity'] for item in cart.values())
        return context

class RemoveFromCartView(View):
    def post(self, request, product_id):
        if request.user.is_authenticated:
            cart_item = CartItem.objects.filter(user=request.user, product_id=product_id).first()
            if cart_item:
                cart_item.delete()
                return JsonResponse({'status': 'success', 'message': 'Товар удален из корзины.'}, status=200)
        return JsonResponse({'status': 'error', 'message': 'Товар не найден.'}, status=404)
