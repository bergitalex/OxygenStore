import os

from django.db import models
from core.models import TimeStampedModel

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(TimeStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    categories = models.ManyToManyField(Category, related_name='products')
    views_count = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name