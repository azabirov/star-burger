import foodcartapp
import star_burger.settings
from .fetch_coordinates import fetch_coordinates

from geopy import distance

from .models import Coordinates

api_key = star_burger.settings.API_KEY_YANDEX


def get_coordinates(address):
    coord, created = Coordinates.objects.get_or_create(
        address=address,
    )
    if created:
        try:
            coords = fetch_coordinates(api_key, address)
            coord.lng, coord.lat = coords
            coord.save()
        except IndexError:
            pass
    return coord


def get_available_restaurants(ordered_item):
    restaurants_ = []
    menu_items = foodcartapp.models.RestaurantMenuItem.objects.filter(product=ordered_item, availability=True)

    for menu_item in menu_items:
        restaurant_ = menu_item.restaurant
        if restaurant_ not in restaurants_:
            restaurants_.append(restaurant_)
    return restaurants_


def get_distance(order_coord, rest_coord):
    return distance.distance((rest_coord.lng, rest_coord.lat), (order_coord.lng, order_coord.lat)).km


def get_distance_between_addresses(cart_address, restaurant_address):
    order_coord = get_coordinates(cart_address)
    rest_coord = get_coordinates(restaurant_address)
    return get_distance(order_coord, rest_coord)


def get_distances_between_restaurants_and_buyer(restaurants, order):
    distances = {}
    order_coord = order.coordinates
    for restaurant in restaurants:
        rest_coord = restaurant.coordinates
        distance = get_distance(order_coord, rest_coord)
        distances[restaurant] = distance
    return distances


def update_cart_restaurant_to_a_nearest_one(restaurants, order):
    distances = get_distances_between_restaurants_and_buyer(restaurants, order)
    order.restaurant = sorted(distances, key=distances.get)[0]
    order.save()


def get_available_restaurants_for_cart(order):
    restaurants = []
    for ordereditem in order.ordered_item.all():
        restaurants_s = []
        menu_items = foodcartapp.models.RestaurantMenuItem.objects.filter(
            product=ordereditem.product,
            availability=True
        )
        for menu_item in menu_items:
            restaurants_s.append(menu_item.restaurant)
        if not restaurants:
            restaurants += restaurants_s
        restaurants = list(set(restaurants_s) & set(restaurants))
    return restaurants
