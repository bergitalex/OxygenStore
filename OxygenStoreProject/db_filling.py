import os
import django
from django.core.files import File

# Указываем путь к настройкам Django проекта
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'OxygenStoreProject.settings')

# Инициализируем Django
django.setup()

# Импорт моделей после инициализации
from products.models import Product, Category

# Словарь с категориями и товарами
data = [
    {
        "name": "От нуля к единице",
        "description": "Питер Тиль предлагает своему читателю убедиться в действенности монополистических бизнес-стратегий на примере опыта огромного количества компаний",
        "price": 899,
        "stock": 20,
        "category": "Books",
        "photo": "OxygenStoreProject/Upload_photos/products/Books/Book1.jpg",
    },
    {
        "name": "Жилет зимний",
        "description": "Зимний жилет, теплая и удобная",
        "price": 5999.99,
        "stock": 30,
        "category": "Clothing",
        "photo": "OxygenStoreProject/Upload_photos/products/Clothing/Jaket1.jpg",
    },
    {
        "name": "Сковорода Basil",
        "description": "Качественная сковорода для дома",
        "price": 1200,
        "stock": 40,
        "category": "Home",
        "photo": "OxygenStoreProject/Upload_photos/products/Home/Pan1.jpg",
    },
    {
        "name": "Сотейник Consul",
        "description": "Удобный сотейник для приготовления пищи",
        "price": 1800,
        "stock": 25,
        "category": "Home",
        "photo": "OxygenStoreProject/Upload_photos/products/Home/Pan2.jpg",
    },
    {
        "name": "Huawei Nova 12i",
        "description": "Современный смартфон с отличными характеристиками",
        "price": 19999.99,
        "stock": 15,
        "category": "Electronics",
        "photo": "OxygenStoreProject/Upload_photos/products/Electronics/Phone1.jpg",
    },
    {
        "name": "Xiaomi Redmi 10",
        "description": "Смартфон Xiaomi с большим экраном",
        "price": 15999.99,
        "stock": 20,
        "category": "Electronics",
        "photo": "OxygenStoreProject/Upload_photos/products/Electronics/Phone2.jpg",
    },
    {
        "name": "Свитшот с принтом",
        "description": "Рубашка с уникальным принтом",
        "price": 1499.99,
        "stock": 60,
        "category": "Clothing",
        "photo": "OxygenStoreProject/Upload_photos/products/Clothing/Shirt1.jpg",
    },
    {
        "name": "Робот-пылесос Xiaomi",
        "description": "Робот-пылесос для дома",
        "price": 12999.99,
        "stock": 10,
        "category": "Appliances",
        "photo": "OxygenStoreProject/Upload_photos/products/Appliances/VacuumRobot1.jpg",
    },
]

# Добавляем категории и товары в базу данных
for item in data:
    category, created = Category.objects.get_or_create(name=item['category'])

    product = Product.objects.create(
        name=item['name'],
        description=item['description'],
        price=item['price'],
        stock=item['stock'],
    )

    product.categories.add(category)

    # Добавляем изображение товара
    if os.path.exists(item['photo']):
        with open(item['photo'], 'rb') as img_file:
            product.photo.save(os.path.basename(item['photo']), File(img_file), save=True)

    product.save()

print("База данных успешно заполнена товарами.")
