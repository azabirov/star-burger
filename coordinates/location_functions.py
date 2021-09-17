from contextlib import suppress

import foodcartapp
from django.conf import settings
from .fetch_coordinates import fetch_coordinates

from geopy import distance

from .models import Coordinates

api_key = settings.API_KEY_YANDEX


def get_coordinates(address):
    coord, created = Coordinates.objects.get_or_create(
        address=address,
    )
    if created:
        with suppress(IndexError):
            coords = fetch_coordinates(api_key, address)
            coord.lng, coord.lat = coords
            coord.save()
    return coord


def get_available_restaurants(ordered_item):
    return ordered_item.menu_items.filter(availability=True).values_list('restaurant', flat=True, distinct=True)


def get_distance(order_coord, rest_coord):
    if order_coord.lng and rest_coord.lng and order_coord.lat and rest_coord.lat:
        return distance.distance((rest_coord.lng, rest_coord.lat), (order_coord.lng, order_coord.lat)).km
    else:
        return None


def get_distance_between_addresses(cart_address, restaurant_address):
    order_coord = get_coordinates(cart_address)
    rest_coord = get_coordinates(restaurant_address)
    return get_distance(order_coord, rest_coord)



def get_available_restaurants_for_cart(order):
    restaurants = []
    for ordereditem in order.ordered_items.all():
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
