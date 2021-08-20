import datetime
import pytz
from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from rest_framework.response import Response
import star_burger.settings
from coordinates.location_functions import \
    get_available_restaurants, update_cart_restaurant_to_a_nearest_one
from star_burger.settings import TIME_ZONE
from .models import Product, Order, OrderedItem
from rest_framework.decorators import api_view
from .serializers import CartDataSerializer


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


@transaction.atomic
@api_view(['POST'])
def register_order(request):
    timezone = pytz.timezone(TIME_ZONE)
    cart_data = request.data
    serializer = CartDataSerializer(data=cart_data)
    serializer.is_valid(raise_exception=True)
    order_ = Order.objects.create(
        firstname=serializer.validated_data["firstname"],
        lastname=serializer.validated_data["lastname"],
        address=serializer.validated_data["address"],
        phonenumber=serializer.validated_data["phonenumber"],
        ordertime=datetime.datetime.now(tz=timezone),
    )
    restaurants = []
    for product_ in serializer.validated_data['products']:
        ordered_item = product_["product"]
        item_order = OrderedItem.objects.create(
            order=order_,
            product=ordered_item,
            quantity=product_["quantity"],
            price=ordered_item.price*product_["quantity"],
        )
        restaurants_ = get_available_restaurants(ordered_item)
        if not restaurants:
            restaurants += restaurants_
        restaurants = list(set(restaurants_) & set(restaurants))
    update_cart_restaurant_to_a_nearest_one(restaurants, order_)
    return Response(serializer.data)
