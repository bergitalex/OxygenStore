
# OxygenStore

OxygenStore — это веб-приложение интернет-магазина, разработанное с использованием Django. Приложение предоставляет возможность пользователям регистрироваться, управлять своей корзиной, оформлять заказы, а также менять информацию о профиле, такую как имя, email и пароль.

## Оглавление

- [Технологии](#технологии)
- [Функциональность](#функциональность)
- [Установка](#yстановка)
- [Настройка SMTP](#настройка-smtp)
- [Использование](#использование)
- [Команды для разработки](#команды-для-разработки)

## Технологии

- **Python** 3.12
- **Django** 5.1.2
- **PostgreSQL** для базы данных
- **Bootstrap** для пользовательского интерфейса
- **Yandex SMTP** для отправки писем
- **JavaScript (jQuery)** для взаимодействия с корзиной

## Функциональность

### 1. Управление пользователями
- **Регистрация и авторизация:** Реализованы кастомные формы регистрации и авторизации с использованием встроенных возможностей Django.
- **Изменение данных профиля:** Пользователи могут обновлять имя, email и пароль с помощью специальных форм с автоматической валидацией и отправкой подтверждений по email через SMTP.
- **Отдельные страницы для редактирования данных:** Реализованы три отдельные страницы для изменения имени, email и пароля.

### 2. Управление товарами и категориями
- **Каталог товаров:** Интуитивно понятный интерфейс позволяет пользователям просматривать каталог товаров, фильтровать их по категориям и добавлять в корзину.
- **Динамические страницы категорий:** Списки категорий и товаров генерируются на основе данных, сохраненных в базе данных.

### 3. Корзина и оформление заказа
- **Добавление товаров в корзину:** Пользователи могут добавлять товары в корзину и изменять количество прямо в корзине.
- **Оформление заказа:** После добавления товаров в корзину пользователи могут перейти к оформлению заказа.
- **Подтверждение заказа:** При подтверждении заказа количество товара на складе автоматически уменьшается.
- **Сохранение адреса и примечаний:** При оформлении заказа пользователь вводит адрес, который сохраняется вместе с заказом в базе данных.

### 4. Управление заказами
- **Личный кабинет:** Пользователь может просматривать свои заказы на отдельной странице. Заказы отображаются в виде сгруппированных блоков для упрощенной навигации.
- **Просмотр деталей заказа:** Для каждого заказа можно просмотреть его состав, общую сумму и адрес доставки.
- **Отмена заказа:** Реализована возможность отмены заказа.

### Установка
1. Клонируйте репозиторий:
   ```bash
   git clone <URL>
   cd OxygenStoreProject
   ```
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Настройте базу данных и примените миграции:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Проверьте данные в config.json
5. Запустите сервер разработки:
   ```bash
   python manage.py runserver
   ```
   
## Настройка SMTP

### Настройка только отправки через SMTP
Настройка SMTP требуется для отправки подтверждений и уведомлений по электронной почте.

### Шаги по настройке:
1. **Настройте почтовый ящик:**
   - Перейдите в раздел **«Почтовые программы»** в настройках Яндекс Почты.
   - Включите опцию **«Разрешить доступ к почтовому ящику с помощью почтовых клиентов» → «С сервера imap.yandex.ru по протоколу IMAP»** и **«Пароли приложений и OAuth-токены»**.
   - Сохраните изменения.

2. **Создайте пароль приложения:**
   - Перейдите на страницу **Пароли приложений** в вашем аккаунте Яндекс ID и нажмите **«Создать новый пароль»**.
   - Выберите тип приложения **«Почта»**.
   - Укажите название пароля (например, название вашего приложения).
   - Нажмите **«Далее»**. Всплывающее окно покажет ваш пароль приложения.
   - **Примечание:** Пароль отображается только один раз. Если вы ввели его неверно и закрыли окно, удалите текущий пароль и создайте новый.

3. **Настройте программу (SMTP):**
   - Адрес почтового сервера: **smtp.yandex.ru**
   - Защита соединения: **SSL**
   - Порт: **465** (или **587**, если соединение без шифрования)
   - Введите ваш логин и пароль приложения для доступа к серверу.

## Использование

1. **Зарегистрируйтесь и войдите на сайт.**
2. **Добавьте товары в корзину и оформите заказ.**
3. **Перейдите в личный кабинет для управления профилем и просмотра заказов.**

## Команды для разработки

- **`python manage.py runserver`** — запуск сервера разработки.
- **`python manage.py makemigrations`** — создание миграций.
- **`python manage.py migrate`** — применение миграций.
- **`python manage.py createsuperuser`** — создание суперпользователя.
