from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from phonenumber_field.modelfields import PhoneNumberField

from coordinates.location_functions import get_coordinates, get_distance, get_available_restaurants_for_cart


class Restaurant(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    address = models.CharField(
        'адрес',
        max_length=100,
        blank=True,
    )
    contact_phone = models.CharField(
        'контактный телефон',
        max_length=50,
        blank=True,
    )

    def findCoordinates(self):
        return get_coordinates(self.address)

    coordinates = property(findCoordinates)

    class Meta:
        verbose_name = 'ресторан'
        verbose_name_plural = 'рестораны'

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def available(self):
        products = (
            RestaurantMenuItem.objects
            .filter(availability=True)
            .values_list('product')
        )
        return self.filter(pk__in=products)


class ProductCategory(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        'название',
        max_length=50
    )
    category = models.ForeignKey(
        ProductCategory,
        verbose_name='категория',
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    price = models.DecimalField(
        'цена',
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    image = models.ImageField(
        'картинка'
    )
    special_status = models.BooleanField(
        'спец.предложение',
        default=False,
        db_index=True,
    )
    description = models.TextField(
        'описание',
        max_length=200,
        blank=True,
    )

    objects = ProductQuerySet.as_manager()

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'

    def __str__(self):
        return self.name


class RestaurantMenuItem(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        related_name='menu_items',
        verbose_name="ресторан",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='menu_items',
        verbose_name='продукт',
    )
    availability = models.BooleanField(
        'в продаже',
        default=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'пункт меню ресторана'
        verbose_name_plural = 'пункты меню ресторана'
        unique_together = [
            ['restaurant', 'product']
        ]

    def __str__(self):
        return f"{self.restaurant.name} - {self.product.name}"


class Order(models.Model):
    STATUS = (
        ('unprocessed', 'Необработанный'),
        ('processed', 'Обработанный'),
    )
    PAYMENT_CHOICES = (
        ('cash', 'Наличностью'),
        ('card', 'Электронно'),
    )

    status = models.CharField(
        'статус',
        choices=STATUS,
        max_length=64,
        default='unprocessed',
    )
    payment = models.CharField(
        'способ оплаты',
        choices=PAYMENT_CHOICES,
        max_length=64,
        default='cash',
    )
    firstname = models.CharField(
        'имя',
        max_length=63,
    )
    lastname = models.CharField(
        'фамилия',
        max_length=63,
    )
    address = models.CharField(
        'адрес',
        max_length=63,
    )
    phonenumber = PhoneNumberField(
        'номер телефона',
    )
    ordertime = models.DateTimeField(
        'время заказа',
    )
    calltime = models.DateTimeField(
        'время звонка',
        null=True,
        blank=True,
    )
    comment = models.TextField(
        'комментарий',
        max_length=256,
        blank=True,
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, null=True, blank=True, verbose_name='ресторан')

    def findCoordinates(self):
        return get_coordinates(self.address)

    coordinates = property(findCoordinates)

    def findDistanceToTheRestaurant(self):
        self_coordinates = self.coordinates
        if self.restaurant and self_coordinates.lng:
            return round(get_distance(self_coordinates, self.restaurant.coordinates), 2)
        return None

    distance_to_restaurant = property(findDistanceToTheRestaurant)

    def findDistanceToAllAvailableRestaurants(self):
        restaurants = get_available_restaurants_for_cart(self)
        self_coordinates = self.coordinates
        if restaurants:
            restaurants_ = {restaurant:round(get_distance(self_coordinates, restaurant.coordinates), 2) if self_coordinates.lng else None for restaurant in restaurants}
            return dict(sorted(restaurants_.items(), key=lambda x: (x[1] is None, x[1])))
        return None

    distances_to_restaurants = property(findDistanceToAllAvailableRestaurants)

    def __str__(self):
        return f"[{self.ordertime.strftime('%Y-%m-%d %H:%M:%S %Z')}] {self.status} {self.firstname} {self.lastname} - {self.phonenumber}"

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'


class OrderedItem(models.Model):
    cart = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='ordered_item',
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='заказанный продукт',
    )
    quantity = models.PositiveIntegerField(
        'количество',
        validators=[MaxValueValidator(50)],
    )
    price = models.DecimalField(
        'цена товара',
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
    )

    def __str__(self):
        return f"{self.cart} - {self.product} {self.quantity}"
