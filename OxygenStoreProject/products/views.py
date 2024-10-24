from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product, Category


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        print('det', context['categories'])
        return context