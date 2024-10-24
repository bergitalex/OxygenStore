from django.views.generic import ListView
from django.views.generic import TemplateView, View
import logging

from products.models import Product, Category

logger = logging.getLogger(__name__)


class MainView(TemplateView):
    template_name = 'core/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем 6 товаров с наибольшим количеством просмотров
        context['popular_products'] = Product.objects.order_by('-views_count')[:6]

        # Получаем все категории для выпадающего списка в хедере
        context['categories'] = Category.objects.all()

        return context

class CategoryProductsView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs['pk'])
        return Product.objects.filter(categories=category).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        context['categories'] = Category.objects.all()
        print('catprod', context['categories'], context['category'])
        return context
