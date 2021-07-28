from rest_framework.serializers import ModelSerializer

from foodcartapp.models import OrderedItem, Order


class OrderItemDataSerializer(ModelSerializer):
    class Meta:
        model = OrderedItem
        fields = ['product', 'quantity']


class CartDataSerializer(ModelSerializer):
    products = OrderItemDataSerializer(allow_empty=False, many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['firstname', 'lastname', 'address', 'phonenumber', 'products']
