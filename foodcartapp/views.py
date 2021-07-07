import datetime
import pytz
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework import status
from rest_framework.response import Response

from star_burger.settings import TIME_ZONE
from .models import Product, Order, OrderedItem

from rest_framework.decorators import api_view


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


@api_view(['POST'])
def register_order(request):
    timezone = pytz.timezone(TIME_ZONE)
    cart_data = request.data
    try:
        cartdatacheck = isinstance(cart_data["firstname"], str) and isinstance(cart_data["lastname"], str) \
                        and isinstance(cart_data["address"], str) and isinstance(cart_data["phonenumber"], (str, int))\
                        and isinstance(cart_data["products"], list) and cart_data["products"]\
                        and cart_data["phonenumber"]
        if cartdatacheck:
            cart = Order.objects.create(
                firstname=cart_data["firstname"],
                lastname=cart_data["lastname"],
                address=cart_data["address"],
                phonenumber=cart_data["phonenumber"],
                ordertime=datetime.datetime.now(tz=timezone),
            )
            for product in cart_data["products"]:
                if isinstance(product["product"], int) and isinstance(product["quantity"], int):
                    ordered_item = Product.objects.get(pk=product["product"])
                    OrderedItem.objects.create(
                        cart=cart,
                        ordered_product=ordered_item,
                        quantity=product["quantity"],
                    )
                else:
                    return Response({"error": "POST data is false or corrupted"}, status=status.HTTP_400_BAD_REQUEST)
            return Response()
    except KeyError:
        pass
    return Response({"error": "POST data is false or corrupted"}, status=status.HTTP_400_BAD_REQUEST)

