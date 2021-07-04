import json
import pytz
import datetime
from django.http import JsonResponse
from django.templatetags.static import static

from star_burger.settings import TIME_ZONE
from .models import Product, Order, OrderedItem


def banners_list_api(request):
    # FIXME move data to db?
    return JsonResponse([
        {
            'title': 'Burger',
            'src': static('burger.jpg'),
            'text': 'Tasty Burger at your door step',
        },
        {
            'title': 'Spices',
            'src': static('food.jpg'),
            'text': 'All Cuisines',
        },
        {
            'title': 'New York',
            'src': static('tasty.jpg'),
            'text': 'Food is incomplete without a tasty dessert',
        }
    ], safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def product_list_api(request):
    products = Product.objects.select_related('category').available()

    dumped_products = []
    for product in products:
        dumped_product = {
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'special_status': product.special_status,
            'description': product.description,
            'category': {
                'id': product.category.id,
                'name': product.category.name,
            },
            'image': product.image.url,
            'restaurant': {
                'id': product.id,
                'name': product.name,
            }
        }
        dumped_products.append(dumped_product)
    return JsonResponse(dumped_products, safe=False, json_dumps_params={
        'ensure_ascii': False,
        'indent': 4,
    })


def register_order(request):
    try:
        timezone = pytz.timezone(TIME_ZONE)
        cart_data = json.loads(request.body.decode())
        cart = Order.objects.create(
            firstname=cart_data["firstname"],
            lastname=cart_data["lastname"],
            address=cart_data["address"],
            phonenumber=cart_data["phonenumber"],
            ordertime=datetime.datetime.now(tz=timezone),
        )
        for product in cart_data["products"]:
            ordered_item = Product.objects.get(pk=product["product"])
            OrderedItem.objects.create(
                cart=cart,
                ordered_product=ordered_item,
                quantity=product["quantity"],
            )
        return JsonResponse({})
    except ValueError:
        return JsonResponse({
            'error': 'ValueError',
        })
