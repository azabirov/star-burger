from django.db import transaction
from django.http import JsonResponse
from django.templatetags.static import static
from django.utils import timezone
from rest_framework.response import Response
from coordinates.location_functions import \
    get_available_restaurants, update_cart_restaurant_to_a_nearest_one
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
    cart_data = request.data
    serializer = CartDataSerializer(data=cart_data)
    serializer.is_valid(raise_exception=True)
    order_ = Order.objects.create(
        firstname=serializer.validated_data["firstname"],
        lastname=serializer.validated_data["lastname"],
        address=serializer.validated_data["address"],
        phonenumber=serializer.validated_data["phonenumber"],
        ordertime=timezone.now(),
    )
    restaurants = []
    for product_ in serializer.validated_data['products']:
        ordered_product = product_["product"]
        item_order = OrderedItem.objects.create(
            order=order_,
            product=ordered_product,
            quantity=product_["quantity"],
            price=ordered_product.price*product_["quantity"],
        )
        restaurants_ = get_available_restaurants(ordered_product)
        if not restaurants:
            restaurants += restaurants_
        restaurants = list(set(restaurants_) & set(restaurants))
    update_cart_restaurant_to_a_nearest_one(restaurants, order_)
    return Response(serializer.data)
